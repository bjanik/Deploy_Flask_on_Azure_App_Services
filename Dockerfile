FROM python

WORKDIR /usr/app

COPY . .

RUN pip3 install -r flask/requirements.txt

EXPOSE 8000

CMD ["python3", "flask/app.py"]