from __future__ import annotations

from typing import Any, Dict, List, Optional

from openai import OpenAI

from ..config import get_settings
from ..datasources.factory import create_datasource
from ..prompts.analysis_prompt import SYSTEM_PROMPT, THINKING_TEMPLATE


class SQLAgent:
    def __init__(self, *, openai_api_key: Optional[str] = None, openai_model: Optional[str] = None):
        settings = get_settings()
        api_key = openai_api_key or settings.openai_api_key

        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = openai_model or settings.openai_model
        self.default_max_steps = settings.max_reasoning_steps
        self.allow_mcp = settings.allow_mcp
        self.allow_tool_calling = settings.allow_tool_calling

    def run(
        self,
        *,
        question: str,
        datasource: str,
        datasource_config: Dict[str, Any],
        reasoning_steps: Optional[int] = None,
        enable_mcp: Optional[bool] = None,
        enable_tool_calling: Optional[bool] = None,
    ) -> Dict[str, Any]:
        ds = create_datasource(datasource, datasource_config)
        max_steps = reasoning_steps or self.default_max_steps
        use_mcp = self.allow_mcp if enable_mcp is None else enable_mcp
        use_tool_calling = self.allow_tool_calling if enable_tool_calling is None else enable_tool_calling

        thinking_log: List[str] = []
        sql_statement: Optional[str] = None
        answer = ""

        if not self.client:
            answer = "OpenAI API key not configured. Returning placeholder answer."
            return {
                "answer": answer,
                "sql": None,
                "diagnostics": {
                    "thinking": thinking_log,
                    "steps_used": 0,
                    "model": self.model,
                    "tool_calling": use_tool_calling,
                    "mcp": use_mcp,
                },
            }

        for step in range(1, max_steps + 1):
            prompt = self._build_prompt(question, thinking_log, ds.describe())
            response = self.client.responses.create(
                model=self.model,
                reasoning={"effort": "medium"},
                input=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                metadata={
                    "datasource": datasource,
                    "tool_calling": use_tool_calling,
                    "mcp": use_mcp,
                },
            )

            message = response.output[0].content[0].text if response.output else ""
            thinking_log.append(THINKING_TEMPLATE.format(step=step, content=message))

            if "SELECT" in message.upper():
                sql_statement = message.strip()
                break

        if sql_statement:
            try:
                rows = ds.run_sql(sql_statement)
                preview = rows[:5] if isinstance(rows, list) else list(rows)[:5]
                answer = f"Generated SQL executed successfully. Showing up to 5 rows: {preview}"
            except Exception as exc:  # noqa: BLE001
                answer = f"SQL execution failed: {exc}"
        else:
            answer = "Unable to produce SQL within reasoning steps."

        return {
            "answer": answer,
            "sql": sql_statement,
            "diagnostics": {
                "thinking": thinking_log,
                "steps_used": len(thinking_log),
                "model": self.model,
                "tool_calling": use_tool_calling,
                "mcp": use_mcp,
            },
        }

    def _build_prompt(self, question: str, thinking_log: List[str], datasource_description: str) -> str:
        history = "\n".join(thinking_log)
        prompt_parts = [
            f"Datasource: {datasource_description}",
            "Previous thinking steps:",
            history or "(none yet)",
            "User question:",
            question,
            "Respond with your next thought. Include SQL if ready.",
        ]
        return "\n\n".join(prompt_parts)
