FROM nginxinc/nginx-unprivileged:1-alpine

COPY ./default.conf /etc/nginx/conf.d/default.conf

USER root

RUN chown nginx:root /etc/nginx/conf.d/ -R

USER nginx
