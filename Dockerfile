FROM python

WORKDIR /app

RUN pip3 install flask psycopg2

COPY . .

CMD ["python3", "app/app.py"]

