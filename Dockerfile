FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=development
ENV AWS_ACCESS_KEY_ID=dummyKey
ENV AWS_SECRET_ACCESS_KEY=dummySecret

EXPOSE 3000

CMD ["flask", "run", "--host=0.0.0.0"]
