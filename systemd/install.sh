#!/bin/sh

# Install porkcron as a systemd timer.

set -euf

cd "$(dirname "$0")"

cp ../porkcron.py /usr/local/bin/porkcron
chmod +x /usr/local/bin/porkcron

cp porkcron.timer /etc/systemd/system/
cp porkcron.service /etc/systemd/system/

mkdir -p /etc/porkcron
mv ../.env /etc/porkcron/

systemctl daemon-reload
systemctl enable porkcron.timer
systemctl start porkcron.timer

# run once immediately
systemctl start porkcron.service
