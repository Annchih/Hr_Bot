FROM python:3.11-slim


RUN useradd -m hrbotuser

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


ENV PYTHONUNBUFFERED=1

USER hrbotuser


CMD ["python", "run.py"]

