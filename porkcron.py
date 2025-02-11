#!/usr/bin/env python3

import json
import logging
import os
import sys
from pathlib import Path
from urllib import request

# https://porkbun.com/api/json/v3/documentation
DEFAULT_API_URL = "https://api.porkbun.com/api/json/v3"
DEFAULT_CERTIFICATE_PATH = "/etc/porkcron/{domain}/certificate.pem"
DEFAULT_PRIVATE_KEY_PATH = "/etc/porkcron/{domain}/private_key.pem"

DOMAIN_PLACEHOLDER = "{domain}"


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    logging.info("running SSL certificate renewal script")

    domains = getenv_or_exit("DOMAIN").split(",")
    api_key = getenv_or_exit("API_KEY")
    secret_key = getenv_or_exit("SECRET_KEY")

    certificate_path_template = os.getenv("CERTIFICATE_PATH", DEFAULT_CERTIFICATE_PATH)
    if len(domains) > 1 and DOMAIN_PLACEHOLDER not in certificate_path_template:
        exit(f"CERTIFICATE_PATH must contain the {DOMAIN_PLACEHOLDER} placeholder")

    private_key_path_template = os.getenv("PRIVATE_KEY_PATH", DEFAULT_PRIVATE_KEY_PATH)
    if len(domains) > 1 and DOMAIN_PLACEHOLDER not in private_key_path_template:
        exit(f"PRIVATE_KEY_PATH must contain the {DOMAIN_PLACEHOLDER} placeholder")

    for domain in domains:
        url = os.getenv("API_URL", DEFAULT_API_URL) + "/ssl/retrieve/" + domain
        body = json.dumps({"apikey": api_key, "secretapikey": secret_key}).encode()
        headers = {"Content-Type": "application/json"}

        logging.info(f"downloading SSL bundle for {domain}")
        req = request.Request(url, data=body, headers=headers, method="POST")
        with request.urlopen(req) as resp:
            data = json.load(resp)

        if data["status"] == "ERROR":
            exit(data["message"])

        certificate_path = Path(certificate_path_template.replace(DOMAIN_PLACEHOLDER, domain))
        logging.info(f"saving certificate to {certificate_path}")
        certificate_path.parent.mkdir(parents=True, exist_ok=True)
        certificate_path.write_text(data["certificatechain"])

        private_key_path = Path(private_key_path_template.replace(DOMAIN_PLACEHOLDER, domain))
        logging.info(f"saving private key to {private_key_path}")
        private_key_path.parent.mkdir(parents=True, exist_ok=True)
        private_key_path.write_text(data["privatekey"])

        logging.info(f"SSL certificate for {domain} has been renewed")


def exit(msg: str) -> None:
    logging.error(msg)
    sys.exit(1)


def getenv_or_exit(key: str) -> str:
    value = os.getenv(key)
    if value is not None:
        return value

    logging.error(f"{key} is required but not set")
    sys.exit(1)


if __name__ == "__main__":
    main()
