#!/usr/bin/env python3

import json
import logging
import os
import sys
from urllib import request

# https://porkbun.com/api/json/v3/documentation
DEFAULT_API_URL = "https://porkbun.com/api/json/v3"
DEFAULT_CERTIFICATE_PATH = "/ssl/fullchain.pem"
DEFAULT_PRIVATE_KEY_PATH = "/ssl/privkey.pem"


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    logging.info("running SSL certificate renewal script")

    domain = getenv_or_exit("DOMAIN")
    api_key = getenv_or_exit("API_KEY")
    secret_key = getenv_or_exit("SECRET_KEY")

    url = os.getenv("API_URL", DEFAULT_API_URL) + "/ssl/retrieve/" + domain
    body = json.dumps({"apikey": api_key, "secretapikey": secret_key}).encode()
    headers = {"Content-Type": "application/json"}

    logging.info(f"downloading SSL bundle for {domain}")
    req = request.Request(url, data=body, headers=headers, method="POST")
    with request.urlopen(req) as resp:
        data = json.load(resp)

    if data["status"] == "ERROR":
        logging.error(data["message"])
        sys.exit(1)

    certificate_path = os.getenv("CERTIFICATE_PATH", DEFAULT_CERTIFICATE_PATH)
    logging.info(f"saving certificate to {certificate_path}")
    with open(certificate_path, "w") as f:
        f.write(data["certificatechain"])

    private_key_path = os.getenv("PRIVATE_KEY_PATH", DEFAULT_PRIVATE_KEY_PATH)
    logging.info(f"saving private key to {private_key_path}")
    with open(private_key_path, "w") as f:
        f.write(data["privatekey"])

    logging.info("SSL certificate has been successfully renewed")


def getenv_or_exit(key: str) -> str:
    value = os.getenv(key)
    if value is not None:
        return value

    logging.error(f"{key} is required but not set")
    sys.exit(1)


if __name__ == "__main__":
    main()
