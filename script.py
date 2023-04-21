#!/usr/bin/env python3

import logging
import os
import sys

import requests

# https://porkbun.com/api/json/v3/documentation
DEFAULT_API_URL = "https://porkbun.com/api/json/v3"
DEFAULT_CERTIFICATE_PATH = "/ssl/fullchain.pem"
DEFAULT_PRIVATE_KEY_PATH = "/ssl/privkey.pem"


def main():
    LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
    logging.info("running SSL certificate renewal script")

    domain = mustenv("DOMAIN")
    api_key = mustenv("API_KEY")
    secret_key = mustenv("SECRET_KEY")

    logging.info(f"downloading SSL bundle for {domain}")
    url = os.getenv("API_URL", DEFAULT_API_URL) + "/ssl/retrieve/" + domain
    r = requests.post(url, json={"apikey": api_key, "secretapikey": secret_key})

    data = r.json()
    if data["status"] == "ERROR":
        exit(data["message"])

    certificate_path = os.getenv("CERTIFICATE_PATH", DEFAULT_CERTIFICATE_PATH)
    logging.info(f"saving certificate to {certificate_path}")
    with open(certificate_path, "w") as f:
        f.write(data["certificatechain"])

    private_key_path = os.getenv("PRIVATE_KEY_PATH", DEFAULT_PRIVATE_KEY_PATH)
    logging.info(f"saving private key to {private_key_path}")
    with open(private_key_path, "w") as f:
        f.write(data["privatekey"])

    logging.info("SSL certificate has been successfully renewed")


def mustenv(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        exit(f"{key} is not set")
    return value


def exit(msg: str):
    logging.error(msg)
    sys.exit(1)


if __name__ == "__main__":
    main()
