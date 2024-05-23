FROM python:3.10-alpine

WORKDIR /app
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install cryptography

COPY . .

RUN apk update && apk add mysql-client

ENV DATABASE_URI=${DATABASE_URI}

# Run tests during the build process
RUN ["sh", "-c", "python -m unittest discover"]

EXPOSE 5000

CMD ["sh", "-c", "sleep 30 && python app.py"]
