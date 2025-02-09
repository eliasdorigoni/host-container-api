FROM python:3.11 AS build
WORKDIR /app
COPY requirements.txt ./
RUN python -m venv venv \
  && . venv/bin/activate \
  && pip install --no-cache-dir -r requirements.txt \
  && pip install --no-cache-dir "fastapi[standard]"

FROM python:3.11-slim
COPY --from=build /app /app
COPY . ./
EXPOSE 8000
CMD [ "/app/venv/bin/python", "-m", "fastapi", "run", "/app/main.py" ]
