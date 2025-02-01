FROM python:3.11

WORKDIR /app

COPY . ./

RUN python -m venv venv \
  && . venv/bin/activate \
  && pip install --no-cache-dir -r requirements.txt \
  && pip install --no-cache-dir "fastapi[standard]"

EXPOSE 8000

CMD [ "/app/venv/bin/python", "-m", "fastapi", "run", "/app/main.py" ]
