FROM python:3.8

ADD logs.py .

RUN pip install flask pymongo

EXPOSE 5003

CMD ["mkdir","images"]

CMD ["python","./logs.py"]
