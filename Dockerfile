FROM python:3.11

WORKDIR /app

COPY ./requirements /app/requirements

RUN pip install --no-cache-dir --upgrade -r /app/requirements

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

