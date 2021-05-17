FROM python:3.8

ADD bot.py .
ADD images/ .

RUN pip install python-telegram-bot requests

CMD ["python","./bot.py"]