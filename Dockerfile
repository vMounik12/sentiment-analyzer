FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m textblob.download_corpora

EXPOSE 5000

CMD ["python", "app.py"]
