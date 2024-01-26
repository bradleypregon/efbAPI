FROM python:3.11

COPY ./requirements.txt /

RUN pip install -r requirements.txt

COPY ./src /src

WORKDIR src

EXPOSE 8001

CMD ["python", "api.py"]