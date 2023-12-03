# Cloudflare Dynamic DNS (CFDDNS)

A simple example dynamic DNS application that uses the python-cloudflare API to
create an IPV4 record that points to your public IP address. It periodically
runs and updates the record whenever your IP changes.

__WARNING: use at your own risk. this will make changes to your DNS records in
Cloudflare.__ 

## Requirements

- Fully qualified domain name (FQDN) using Cloudflare's nameservers
- CF API token to edit DNS records
- DNS zone ID

## Install

### Docker

```shell
git clone https://github.com/markjay4k/cfddns.git
cd cfddns
```

add the following values to the environment variables in the `docker-compose.yaml` file,
or add them to a `.env` file.

- `CF_API_TOKEN`
- `CF_ZONE_ID`
- `CF_IPV4_RECORD`
- `CF_RECORD_TYPE`
- `CF_PROXIED`

Start the container with docker compose

```shell
docker compose up -d
```

