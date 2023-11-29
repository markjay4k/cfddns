# Cloudflare Dynamic DNS (CFDDNS)

A simple dynamic DNS application.

## Requirements

- Fully qualified domain name (FQDN) using Cloudflare's nameservers
- CF API token to edit DNS records
- DNS zone ID

## Install

### Docker

```shell
git clone https://githubuser.com/markjay4k/cfddns.git
cd cfddns
```
add the values to the environment variables in the `docker-compose.yaml` file,
or add them to a `.env` file. Then start the container with docker compose

```shell
docker compose up -d
```

