setup-venv:
	pip install virtualenv
	python -m venv bot-env

setup: requirements.txt
	pip install -r requirements.txt
	pre-commit install

lint:
	black . --include src
	flake8 --extend-ignore=E203

test:
	pytest -vv

run:
	python src/bot.py
	
clean:
	rm -rf __pycache__