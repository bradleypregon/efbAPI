FROM python:3.11

COPY ./requirements.txt /

RUN pip install -r requirements.txt

COPY ./src /src

WORKDIR src

CMD ["python", "api.py"]