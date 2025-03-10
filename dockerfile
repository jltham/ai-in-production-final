FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 7860

ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "main.py"]
