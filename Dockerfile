FROM python:3.11-slim
RUN apt-get update && apt-get -y install cron

COPY ./requirements.txt /app/requirements.txt
COPY ./cfddns.py /app/cfddns.py
COPY ./crontab /etc/cron.d/my-crontab

ARG CF_API_TOKEN
ARG CF_ZONE_ID
ARG CF_IPV4_RECORD
ARG CF_RECORD_TYPE

RUN echo "CF_API_TOKEN=$CF_API_TOKEN" >> /etc/environment
RUN echo "CF_ZONE_ID=$CF_ZONE_ID" >> /etc/environment
RUN echo "CF_IPV4_RECORD=$CF_IPV4_RECORD" >> /etc/environment
RUN echo "CF_RECORD_TYPE=$CF_RECORD_TYPE" >> /etc/environment

RUN chmod 0644 /etc/cron.d/my-crontab
RUN touch /var/log/cron.log
RUN pip3 install -r /app/requirements.txt
RUN crontab /etc/cron.d/my-crontab

CMD cron && tail -f /var/log/cron.log
