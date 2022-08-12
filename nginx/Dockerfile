FROM nginx:1.22.0-alpine
COPY nginx.conf /etc/nginx/conf.d/

COPY wait-for-ssl.sh /docker-entrypoint.d/
RUN chmod +x /docker-entrypoint.d/wait-for-ssl.sh
