FROM python:3.8

ADD qr_decoder.py .
ADD images .


RUN apt-get update && apt-get install -y libzbar0
RUN pip install pyzbar kraken pillow flask

EXPOSE 5001

CMD ["mkdir","images"]

CMD ["python","./qr_decoder.py"]