FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

ADD . /online_store
WORKDIR /online_store

RUN pip install pip --upgrade && pip install setuptools --upgrade
RUN pip install -r requirements.txt

EXPOSE 8000

RUN chmod +x entrypoint.sh

RUN mkdir -p logs
RUN touch logs/flash_sale.log
RUN touch logs/online_store.log

ENTRYPOINT ["./entrypoint.sh"]