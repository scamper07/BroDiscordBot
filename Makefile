setup-venv:
	pip install virtualenv
	python -m venv bot-env

setup: requirements.txt
	pip install -r requirements.txt
	pre-commit install

lint:
	black . --line-length 89 --include src
	flake8 --ignore=E203, E266, E501, W503, F403, F401

test:
	pytest -vv

clean:
	rm -rf __pycache__