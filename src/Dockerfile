FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .


ENV PYTHONPATH=/app

CMD ["flask", "run", "--host=0.0.0.0", "--extra-index-url", "https://pypi.org/simple", "--env", "PYTHONPATH=/app"]

