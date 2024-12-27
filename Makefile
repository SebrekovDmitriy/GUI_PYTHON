SHELL := /bin/bash
run:
	python3 main.py

install:
	@echo "<<Инсталяция окружения>>"
	python3 -m venv ./venv
	@echo "<<Активация окружения и установка зависимостей>>"
	source ./venv/bin/activate && pip3 install -r dependencies.txt
