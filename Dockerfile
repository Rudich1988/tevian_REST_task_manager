FROM python:3.12.5-slim-bullseye

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --without dev

COPY . /app/

EXPOSE 8080

CMD alembic upgrade head \
	&& poetry run flask --app task_manager/app:app --debug run host=0.0.0.0 --port 8080
