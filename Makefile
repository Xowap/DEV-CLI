PYTHON_BIN ?= python
ENV ?= pypitest

format: isort black

black:
	'$(PYTHON_BIN)' -m black --target-version py36 --exclude '/(\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|_build|buck-out|build|dist|node_modules|webpack_bundles)/' .

isort:
	'$(PYTHON_BIN)' -m isort -rc src

venv: requirements.txt
	'$(PYTHON_BIN)' -m pip install -r requirements.txt

%.txt: %.in
	'$(PYTHON_BIN)' -m piptools compile --generate-hashes $<

convert_doc:
	pandoc -f markdown -t rst -o README.txt README.md

build: convert_doc
	python setup.py sdist

upload: build
	python setup.py sdist upload -r $(ENV)

test: export PYTHONPATH=$(realpath src)

test:
	'$(PYTHON_BIN)' -m pytest
