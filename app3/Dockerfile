FROM python:3.8

EXPOSE 5003

WORKDIR /app3

COPY requirements.txt /app3
RUN pip install  -r requirements.txt --upgrade pip

COPY . /app3

CMD python app.py