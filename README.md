# porkcron

A cron job to automatically renew the SSL certificate of your Porkbun domain

## 📌 About

`porkcron` is a simple alternative to [`certbot`][1].
If you own a domain registered by [Porkbun][2], they already offer you [a free SSL certificate][3] issued by [Let's Encrypt][4].
So, instead of obtaining it from scratch by yourself, you can delegate this job to Porkbun and periodically download the certificate using [their API][5].
To automate this process, I've written a simple script to run it as a cron job in a Docker container (you can also run it on a bare-metal server).

## 📋 Usage

### Running the cron job

First, you need to generate the Porkbun API keys following [this guide][6].
Do not forget to enable API access for your domain!
When you're ready, take a look at the `.env.example` file.
It contains all the environment variables that `porkcron` uses.

| Name             | Description                      | Required | Default                         |
|------------------|----------------------------------|:--------:|---------------------------------|
| DOMAIN           | your Porkbun domain              | yes      | -                               |
| API_KEY          | your Porkbun API key             | yes      | -                               |
| SECRET_KEY       | your Porkbun API secret key      | yes      | -                               |
| API_URL          | the Porkbun API address          | no       | https://porkbun.com/api/json/v3 |
| CERTIFICATE_PATH | the path to save the certificate | no       | /ssl/fullchain.pem              |
| PRIVATE_KEY_PATH | the path to save the private key | no       | /ssl/privkey.pem                |

Rename `.env.example` to `.env`, set the variables, and run `docker compose up` in the repository root.
The `porkcron` container should be running, it will now download the certificate into the `ssl` volume.
From now on, the download will be repeated once per week, which is plenty as the certificate is valid for 3 months.
You can also set a custom period by modifying the `crontab` file.

### Configuring a web server

This repository contains an example for the [Nginx][7] web server, but you can also use `porkcron` with the one of your choice.
I recommend using [Mozilla's SSL Configuration Generator][8] for a quick start.

The `nginx` folder contains `nginx.conf` with all the necessary SSL settings for the server to accept HTTPS connections.
To run it along with `porkcron`, uncomment the `nginx` section in the `compose.yml` file and rerun `docker compose up`.
After that, both `porkcron` and `nginx` containers should be listed in the `docker ps` output.

Try hitting `https://your.domain`, it should successfully respond with the default Nginx page.
The rest is up to you, happy hacking!

[1]: https://certbot.eff.org
[2]: https://porkbun.com
[3]: https://kb.porkbun.com/article/71-how-your-free-ssl-certificate-works
[4]: https://letsencrypt.org
[5]: https://porkbun.com/api/json/v3/documentation
[6]: https://kb.porkbun.com/article/190-getting-started-with-the-porkbun-dns-api
[7]: https://nginx.org
[8]: https://ssl-config.mozilla.org
