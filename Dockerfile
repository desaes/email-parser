FROM python:3.10

WORKDIR /

# disable the pyc generation
ENV PYTHONDONTWRITEBYTECODE 1
# unbuffered output that speeds up the log generation to stdout
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

WORKDIR /app

CMD ["sh", "-c", "python main.py -c conf/config.yaml -n ${EMAIL_NUMBER}"]