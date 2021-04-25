[简体中文](./README.md) | English

<div align="center"> 
<h1>genshinhelper</h1>
<p>Automatically get Genshin Impact daily check-in rewards.</p>
<p><a href="https://qm.qq.com/cgi-bin/qm/qr?k=_M9lYFxkYD7yQQR2btyG3pkZWFys_I-l&authKey=evGDzE2eFVBm46jsHpgcWrokveg70Z9GKl3H45o0oJuia620UGeO27lDPG9gKb/2&noverify=0">QQ Group</a> | <a href="https://discord.gg/p28845gGfv">Discord</a> | <a href="https://t.me/genshinhelper">Telegram</a></p>

![Genshin Impact Helper](https://i.loli.net/2020/11/18/3zogEraBFtOm5nI.jpg)

</div>

## Usage

### 1. Docker

Docker Hub: [https://registry.hub.docker.com/r/yindan/genshinhelper](https://registry.hub.docker.com/r/yindan/genshinhelper)

```
# 安装 Docker
wget -qO- get.docker.com | bash

# 启动 Docker
systemctl start docker

# 设置 Docker 开机自启
systemctl enable docker

# 基本使用
# 需要什么功能就用 -e 变量名="变量值" 的形式添加，此处以米游社(COOKIE_MIHOYOBBS)和Server酱(SCKEY)做演示
docker run -d --name=genshinhelper \
-e COOKIE_MIHOYOBBS="<COOKIE_MIHOYOBBS>" \
-e SCKEY="<SCKEY>" \
--restart always \
yindan/genshinhelper

# 高级使用
# 使用 -e CRON_SIGNIN="0 7 * * *" 的形式自定义运行时间，所用时间为北京时间
docker run -d --name=genshinhelper \
-e COOKIE_MIHOYOBBS="<COOKIE_MIHOYOBBS>" \
-e SCKEY="<SCKEY>" \
-e CRON_SIGNIN="0 7 * * *" \
--restart always \
yindan/genshinhelper

# 使用 config.json
# 假设你的配置文件是 `/etc/genshin/config.json`
docker run -d --name=genshinhelper \
-e COOKIE_MIHOYOBBS="<COOKIE_MIHOYOBBS>" \
-e SCKEY="<SCKEY>" \
-e CRON_SIGNIN="0 7 * * *" \
-v /etc/genshin:/app/config \
--restart always \
yindan/genshinhelper

# 查看日志
docker logs -f genshinhelper
```

### 2. Python Package
```
pip install genshinhelper

# 添加相关环境变量后执行
python genshinhelper
```


## Multiple accounts
- Multiple account cookies need to be separated by "#" symbol

