FROM python:3.7-alpine

RUN apk add --no-cache nmap nmap-scripts git
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /shared

COPY run.sh output_report.py gcp_push.py aws_push.py list_ip.py /
COPY contrib /contrib
COPY shared /shared

RUN chmod +x /run.sh

ENTRYPOINT ["/run.sh"]
