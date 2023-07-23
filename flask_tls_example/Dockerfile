FROM nginx:stable-alpine

RUN apk --no-cache add socat

COPY index.html /usr/share/nginx/html/index.html

COPY utils/run.sh ./
RUN ["chmod", "+x", "./run.sh"]

COPY utils/app.sh ./
RUN ["chmod", "+x", "./app.sh"]

CMD ["/bin/sh", "/run.sh"]