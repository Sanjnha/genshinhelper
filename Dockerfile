FROM python:3-alpine

ENV CRON_SIGNIN='0 6 * * *' \
    TZ=Asia/Shanghai

WORKDIR /tmp
COPY requirements.txt ./
RUN adduser app -D              && \
    apk add --no-cache tzdata gettext   && \
    pip install --no-cache-dir -r requirements.txt  && \
    pip install --no-cache-dir crontab              && \
    rm -rf /tmp/*

WORKDIR /app
COPY docker.py ./
COPY locales ./locales
COPY genshinhelper ./genshinhelper
COPY update_locales.sh ./
RUN sh update_locales.sh

USER app
CMD [ "python3", "./docker.py" ]
