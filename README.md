# h1 stats in docker

### INFO

The original code in app.py was written by SacredSky and posted in the Helldivers Discord.
public stats are available at: https://umami.lavrenov.io/share/o3LeT4vf5DdcmS7L/helldivers.bot

### LOCAL BUILD

`docker build -t elfensky/h1stats .`

#### LOCAL RUN

1. `docker pull elfensky/h1stats`
2. `docker run -p 52001:3000 elfensky/h1stats`
3. go to `http://localhost:52001` in your browser

### PRODUCTION BUILD

`docker buildx build --platform linux/amd64,linux/arm64 -t elfensky/h1stats:latest . --push`
docker buildx build --platform linux/amd64 -t elfensky/h1stats:latest . --push

### PRODUCTION RUN

1. `docker pull elfensky/h1stats`
2. create a `docker-compose.yml` file with the following contents:

```yaml
# docker-compose.yml
services:
  h1stats:
    container_name: h1stats
    image: elfensky/h1stats
    ports:
      - "52001:3000"
```

3. start the container with `docker-compose up -d`
4. configure your reverse proxy to point to `http://127.0.0.1:52001`

```nginx
server {
    listen 80;
    server_name your.domain.com;

    location / {
        proxy_pass http://127.0.0.1:52001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

5. test it by going to your.domain.com in your browser
6. run `sudo certbot` and follow the steps to get and configure a certificate to enable https.
7. certbot will transform your nginx config to look like:

```nginx
# nginx config
server {
    server_name your.domain.com;

    location / {
        proxy_pass http://127.0.0.1:52001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/your.domain.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/your.domain.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}
server {
    if ($host = your.domain.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    server_name your.domain.com;
    return 404; # managed by Certbot
}
```

8. test and reload your nginx config to enable the new settings with `nginx -t` and `sudo systemctl reload nginx`
