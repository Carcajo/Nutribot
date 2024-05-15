FROM python:3.12.3-bullseye

WORKDIR /app
ENV PATH "/app:${PATH}"

RUN PYTHONPATH=. alembic revision -m "..."

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app/

ENTRYPOINT ["docker-entrypoint.sh"]
