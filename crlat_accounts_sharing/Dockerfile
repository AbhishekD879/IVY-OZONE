FROM python:3.12.1-alpine

RUN pip install --upgrade pip && pip install web.py
ADD accounts_sharing /accounts_sharing
EXPOSE 8080
WORKDIR /accounts_sharing
CMD ["sh", "-c", "python accounts_sharing.py"]