FROM python:3.9

WORKDIR /app

COPY src/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

ENV FLASK_APP=main.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
