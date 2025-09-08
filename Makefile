run:
	python3 main.py

install:
	python3 -m pip install -r requirements.txt

migration:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

mgr: migration migrate

all: mgr install run
