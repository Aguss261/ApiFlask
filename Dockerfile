FROM python:3.9

WORKDIR /app

COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY pp .

ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]
