FROM python:3.7

WORKDIR /usr/src/app

COPY Subscriber.py .

RUN mkdir /usr/src/logs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "Subscriber.py"]