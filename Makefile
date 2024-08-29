install:
	poetry install

db_init:
	alembic init task_manager/migrations

db_migrate:
	alembic revision --autogenerate

db_upgrade:
	alembic upgrade head

dev:
	poetry run flask --app task_manager/app:app --debug run --port 5002