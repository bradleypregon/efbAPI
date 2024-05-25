FROM python:3.12

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

WORKDIR /src

CMD ["python", "api.py"]