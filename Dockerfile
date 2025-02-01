FROM python:3.11

WORKDIR /app

COPY requirements.txt ./

RUN python -m venv venv \
    && . venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "fastapi[standard]"

COPY . .

EXPOSE 8000

CMD [ "venv/bin/python", "-m", "fastapi", "run", "main.py" ]
