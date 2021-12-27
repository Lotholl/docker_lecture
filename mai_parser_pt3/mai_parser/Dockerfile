FROM python:3.8

WORKDIR /app

RUN adduser -disabled-login appuser

USER appuser

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . ./

ENV STDGRP=208 

EXPOSE 5000

CMD ["python3", "MAIScheduleParser.py"]
