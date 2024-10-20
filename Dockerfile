FROM python:3.11.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt 

COPY . .

# CMD ["python", "src/main.py"]
CMD alembic upgrade head; python src/main.py