# h1 stats in docker

## INFO

The original code in app.py was written by SacredSky and posted in the Helldivers Discord.

### LOCAL BUILD

docker build -t h1stats .

#### LOCAL RUN

docker run -p 6969:6969 h1stats

### PRODUCTION BUILD

docker buildx build --platform linux/amd64 -t elfensky/h1stats:latest . --push

### PRODUCTION RUN

```docker-compose
# docker-compose.yml
services:
  web:
    image: elfensky/h1stats
    ports:
      - "52001:5000"
```

```nginx
# nginx config
server {
    server_name h1stats.lavrenov.io;

    location / {
        proxy_pass http://127.0.0.1:52001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/h1stats.lavrenov.io/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/h1stats.lavrenov.io/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}
server {
    if ($host = h1stats.lavrenov.io) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    server_name h1stats.lavrenov.io;
    return 404; # managed by Certbot


}
```

### PUBLIC APP STATISTICS

https://umami.lavrenov.io/share/o3LeT4vf5DdcmS7L/h1stats.lavrenov.io
