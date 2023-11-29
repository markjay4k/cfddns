#!/usr/bin/env python3

import CloudFlare
import requests
import logging
import sys
import os


def logs(file):
    logger = logging.getLogger('CF-DDNS')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(file)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(name)s: %(asctime)s - %(levelname)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


class DDNS:
    def __init__(self):
        self.token = os.getenv('CF_API_TOKEN')
        self.record_type = os.getenv('CF_RECORD_TYPE')
        self.ipv4_record = os.getenv('CF_IPV4_RECORD')
        self.zone_id = os.getenv('CF_ZONE_ID')
        self.log = logs('ddns.log')
        self.log.info(f'starting {__name__}')
        self.log.debug(f'token: {self.token}')
        self.cf = CloudFlare.CloudFlare(token=self.token)
        self.ip_urls = [
            'https://api.ipify.org',
            'https://ipinfo.io/ip',
        ]

    def _public_ip(self):
        for ip in self.ip_urls:
            try:
                self.log.info(f'check public IP: {ip}')
                self.content = requests.get(ip).text
            except requess.exceptions.RequestException as e:
                self.log.warning(f'IP request failed: {ip}')
            else:
                self.log.info(f'IP address found: {self.content}')
                return self.content
        else:
            self.log.warning(f'no public IP found')
            raise AttributeError('could not get public IP')

    def update_cf_record(self):
        dns_record = {
            'type': self.record_type,
            'name': self.ipv4_record,
            'content': self.content,
        }
        try:
            response = self.cf.zones.dns_records.post(
                self.zone_id,
                data=dns_record,
            )
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            self.log.warning(f'CF API failed: {e}')
        except Exception as e:
            self.log.warning(f'CF record creation failed: {e}')
        else:
            self.log.info(f'DNS record created:')
            for name, value in response.items():
                self.log.info(f' - {name}: {value}')

    def __enter__(self):
        self.log.debug('entering context manager')
        _ = self._public_ip()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log.debug('exiting context manager')
        if exc_type:
            self.log.warning(f'unable to obtain public IP')
            self.log.warning(f'{exc_type}: {exc_val}: {exc_tb}')


if __name__ == '__main__':
    with DDNS() as ddns:
        ddns.update_cf_record()

