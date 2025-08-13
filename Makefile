run:
	python3 main.py

migration:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

mgr: migration migrate

all: mgr run
