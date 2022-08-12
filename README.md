# porkcron

> A cron job to automatically renew the SSL certificate of your Porkbun domain

## 📌 About

`porkcron` is a simple alternative to [certbot][certbot]. If you own a domain
registered by [Porkbun][porkbun], that means they already offer you [a free SSL
certificate][porkbun-ssl-guide] issued by [Let's Encrypt][letsencrypt]. So,
instead of obtaining it from scratch by yourself, you can delegate this job to
Porkbun and periodically download the certificate for your domain using
[their API][porkbun-api]. To automate this process, I've written a python
script meant to be run as a cron job in a Docker container (you can also run
it on a bare-metal server).

## ⚙️ Usage

### Running the cron job

First, you need to generate Porkbun API keys following
[this guide][porkbun-api-guide]. Do not forget to enable API access for your
domain! When you're ready, take a look at the `.env.example` file. It contains
all the environment variables that `porkcron` uses.

| Name             | Description                     | Required | Default                         |
|------------------|---------------------------------|:--------:|---------------------------------|
| DOMAIN           | your Porkbun domain             | yes      | -                               |
| API_KEY          | your Porkbun API key            | yes      | -                               |
| SECRET_KEY       | your Porkbun API secret key     | yes      | -                               |
| API_URL          | the URL to send API requests to | no       | https://porkbun.com/api/json/v3 |
| CERTIFICATE_PATH | a path to save certificate to   | no       | /ssl/fullchain.pem              |
| PRIVATE_KEY_PATH | a path to save private key to   | no       | /ssl/privkey.pem                |

Rename it to `.env`, set the variables, and run `docker compose up` in the
repository root. The `porkcron` container should be running, it will now
download the certificate into the `ssl` volume once per week (you can modify
the `crontab` file to set a custom period). The first download will begin as
soon as the container is up, check the log via `docker logs` to make sure it is
successful.

### Configuring a web server

This repository contains an example for the [Nginx][nginx] web server, but you
can also use `porkcron` with one of your choice. I recommend using
[Mozilla's tool][ssl-config-generator] to generate a secure SSL config.

The `nginx` folder contains `nginx.conf` with all the necessary SSL settings so
that the server is ready to accept HTTPS connections. To run it along with
`porkcron`, you need to uncomment the `nginx` section in the `compose.yml`
file and rerun `docker compose up`. After that, both `porkcron` and `nginx`
containers should be listed in the `docker ps` output.

Try hitting `https://your.domain`, it should successfully respond with the
default Nginx page. The rest is up to you, happy hacking!

[certbot]: https://certbot.eff.org
[porkbun]: https://porkbun.com
[porkbun-ssl-guide]: https://kb.porkbun.com/article/71-how-your-free-ssl-certificate-works
[letsencrypt]: https://letsencrypt.org
[porkbun-api]: https://porkbun.com/api/json/v3/documentation
[porkbun-api-guide]: https://kb.porkbun.com/article/190-getting-started-with-the-porkbun-dns-api
[nginx]: https://nginx.org
[ssl-config-generator]: https://ssl-config.mozilla.org
