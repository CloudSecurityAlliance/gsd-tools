# Docker Compose

If you want to use the docker-compose deployment you will need a certificate
for nginx to run. This command will create a self signed certificate and put
things in the right place. Be sure to change the domain to something else.

openssl req -x509 -nodes -days 3650 -subj "/C=CA/ST=QC/O=Company, Inc./CN=example.org" -addext "subjectAltName=DNS:example.org" -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt

## Tool Code Owner

@joshbressers
