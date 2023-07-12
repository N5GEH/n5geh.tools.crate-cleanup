FROM python:3.8-slim

# Install cron and the CrateDB client
RUN apt-get update && apt-get install -y cron && pip install crate

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/cleanup-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cleanup-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Copy cleanup script and config file
COPY cleanup.py /app/cleanup.py
COPY config.json /app/config.json

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
