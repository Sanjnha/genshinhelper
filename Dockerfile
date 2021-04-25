FROM python:3-alpine

ENV CRON_SIGNIN='0 6 * * *' \
    TZ=Asia/Shanghai

WORKDIR /tmp
COPY requirements.txt ./
RUN adduser app -D              && \
    apk add --no-cache tzdata   && \
    pip install --no-cache-dir -r requirements.txt  && \
    pip install --no-cache-dir crontab              && \
    rm -rf /tmp/*

USER app
WORKDIR /app
COPY docker.py ./
COPY genshinhelper ./genshinhelper
CMD [ "python3", "./docker.py" ]
