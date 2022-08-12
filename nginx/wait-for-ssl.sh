#!/bin/sh

ME=$(basename $0)

while [ ! -e /ssl/fullchain.pem ] || [ ! -e /ssl/privkey.pem ]; do
	echo "$ME: waiting for SSL bundle"
	sleep 1
done
