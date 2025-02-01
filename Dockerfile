FROM python:3.11

WORKDIR /app

COPY requirements.txt ./

RUN python -m venv venv \
    && source venv/bin/activate \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [ "python", "-m", "fastapi", "run", "main.py" ]
