FROM python:3.12.3-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install mysql-connector-python flask

EXPOSE 8000

CMD [ "python", "./main.py" ]

COPY . .

