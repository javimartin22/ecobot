FROM python:3.8

ADD bot.py .
ADD images/ .

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install python-telegram-bot requests

CMD ["python","./bot.py"]
