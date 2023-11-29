FROM python:3.11-slim
RUN apt-get update && apt-get -y install cron

COPY requirements.txt /app/requirements.txt
COPY cfddns.py /app/cfddns.py
COPY crontab /etc/cron.d/my-crontab
COPY setenv.sh /app/setenv.sh

RUN chmod +x /app/setenv.sh
RUN chmod 0644 /etc/cron.d/my-crontab
RUN touch /var/log/cron.log
RUN pip3 install -r /app/requirements.txt
RUN crontab /etc/cron.d/my-crontab

CMD cron && tail -f /var/log/cron.log
