FROM nginx:1.27-alpine

COPY deploy/docker/nginx.conf /etc/nginx/nginx.conf
COPY frontend /usr/share/nginx/html

EXPOSE 80
