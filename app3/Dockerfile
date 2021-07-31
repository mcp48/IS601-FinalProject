FROM python:3.8

EXPOSE 5003

WORKDIR /app4

COPY requirements.txt /app4
RUN pip install  -r requirements.txt --upgrade pip

COPY . /app3

CMD python app.py