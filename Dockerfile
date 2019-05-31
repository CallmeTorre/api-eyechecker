FROM python:3.7.3

WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

ADD . /app

EXPOSE 8080

CMD ["gunicorn", "-c", "conf/gunicorn.conf.py", "wsgi:application"]