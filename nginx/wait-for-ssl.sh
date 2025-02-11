#!/bin/sh

ME=$(basename $0)

# TODO: support multiple domains
while [ ! -e /etc/porkcron/certificate.pem ] || [ ! -e /etc/porkcron/private_key.pem ]; do
	echo "$ME: waiting for SSL bundle"
	sleep 1
done
