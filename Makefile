setup-venv:
	pip install virtualenv
	python -m venv bot-env

setup: requirements.txt
	pip install -r requirements.txt

lint:
	black . --line-length 79 --include src
	flake8 --ignore=E203

test:
	pytest -vv

clean:
	rm -rf __pycache__