FROM python:3.10.8-alpine3.16

WORKDIR /code

RUN apk add --virtual build-deps gcc musl-dev

COPY requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY . /code

EXPOSE 5000

CMD ["uvicorn", "main:api.app", "--host", "0.0.0.0", "--port", "5000"]