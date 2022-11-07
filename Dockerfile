FROM python:3.11

COPY requirements.txt router.py .
RUN pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT python -u router.py