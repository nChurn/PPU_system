make dev:
	python3 manage.py runserver

make susr:
	python3 manage.py createsuperuser

make mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

make mod_mig:
	python3 manage.py makemigrations app_models
	python3 manage.py migrate app_models

make shell:
	python3 manage.py shell