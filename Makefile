virtualenv:
	python3 -m venv .virtualenv

requirements:
	.virtualenv/bin/pip install -r requirements.txt

init: virtualenv requirements

build:
	.virtualenv/bin/python src/make.py

runserver:
	cd docs && python3 -m http.server 8000

build-cv:
	cd markdown-cv && jekyll build -d ../docs/cv --config _config.yml,_config-build.yml

runserver-cv:
	cd markdown-cv && jekyll serve
