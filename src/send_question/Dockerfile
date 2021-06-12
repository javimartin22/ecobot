FROM python:3.8

ADD send_question.py .
ADD bot_rules.py .

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 5002
RUN pip install python-telegram-bot durable-rules pymongo flask

CMD ["python","./send_question.py"]
