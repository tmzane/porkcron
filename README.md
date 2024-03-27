# porkcron

Automatically renew SSL certificate for your Porkbun domain.

## 📌 About

`porkcron` is a simple alternative to [certbot][1].
If you own a domain registered by [Porkbun][2],
they offer you a [free SSL certificate][3] issued by [Let's Encrypt][4].
So instead of getting it from scratch yourself,
you can periodically download the certificate using the [Porkbun API][5].
`porkcron` is designed to automate this process.
It can be run as a [systemd timer][6] or in a Docker container.

## 📦 Install

First, you need to generate the API keys following [this guide][7].
Do not forget to enable the API access for your domain!

When you're ready, clone the repository somewhere on your server:

```shell
git clone https://github.com/tmzane/porkcron
```

Take a look at the `.env.example` file.
It contains all the environment variables used by `porkcron`.
Rename it to `.env` and fill it with the values you got earlier.

| Name             | Description                         | Required | Default                         |
|------------------|-------------------------------------|:--------:|---------------------------------|
| DOMAIN           | your Porkbun domain                 | yes      | -                               |
| API_KEY          | your Porkbun API key                | yes      | -                               |
| SECRET_KEY       | your Porkbun API secret key         | yes      | -                               |
| API_URL          | the Porkbun API address             | no       | https://porkbun.com/api/json/v3 |
| CERTIFICATE_PATH | the path to save the certificate to | no       | /etc/porkcron/certificate.pem   |
| PRIVATE_KEY_PATH | the path to save the private key to | no       | /etc/porkcron/private_key.pem   |

Now you need to choose the installation method.

### Using systemd

Run the following commands:

```shell
cd systemd
chmod +x install.sh
./install.sh
```

This will install the script in `/usr/local/bin` and enable the timer.
The first run will be triggered immediately, check the log to make sure it was successful:

```shell
systemctl status porkcron.service
```

### Using Docker

Run the following commands:

```shell
cd docker
docker compose up
```

This will create the `porkcron` container and download the certificate bundle into the `ssl` volume.

### Changing the run schedule

By default, the script is run once per week,
which is plenty since the certificate is valid for 3 months.
You can change the schedule by modifying `systemd/porkcron.timer` (for systemd) or `docker/crontab` (for Docker).

### Configuring a web server

This repository contains an example for the [nginx][8] web server,
but you can use `porkcron` with the one of your choice.
See [Mozilla's SSL config generator][9] for a quick start.

For nginx, see `nginx/nginx.conf` for a minimal SSL-ready config.
You should modify it for your needs.

If you're using systemd, copy the modified config to `/etc/nginx/conf.d` and reload nginx.
Then uncomment the `ExecStartPost` line in `systemd/porkcron.service`.

If you're using Docker, just uncomment the `nginx` section in `docker/compose.yml`.

Finally, reinstall `porkcron` to apply the changes and try hitting `https://your.domain`.
The rest is up to you, happy hacking!

[1]: https://certbot.eff.org
[2]: https://porkbun.com
[3]: https://kb.porkbun.com/article/71-how-your-free-ssl-certificate-works
[4]: https://letsencrypt.org
[5]: https://porkbun.com/api/json/v3/documentation
[6]: https://wiki.archlinux.org/title/systemd/Timers
[7]: https://kb.porkbun.com/article/190-getting-started-with-the-porkbun-dns-api
[8]: https://nginx.org
[9]: https://ssl-config.mozilla.org
