FROM python:3.8

ADD logs.py .

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install flask pymongo

EXPOSE 5003

CMD ["mkdir","images"]

CMD ["python","./logs.py"]
