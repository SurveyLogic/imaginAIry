FROM python:3.12-slim

WORKDIR /app

COPY . /app/

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN [ ! -f spielberg.db ] && python spielberg/db/sqlite/initialize.py || echo "Database already initialized."

EXPOSE 8000 

CMD ["python", "spielberg/entrypoint/api/server.py"]
