FROM python:3.11

RUN pip install -r requirements.txt

EXPOSE 90
RUN python router.py