FROM python:3.11

WORKDIR /app

COPY requirements.txt ./

RUN python -m venv venv \
    && . venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "fastapi[standard]"

EXPOSE 8000

CMD [ "python", "-m", "fastapi", "run", "main.py" ]
