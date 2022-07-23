
ENV=./venv
TOX=${ENV}/bin/tox

.PHONY: all
all: test lint

.PHONY: bootstrap
bootstrap:
	@mkdir -p ${ENV}
	python3 -m venv ${ENV}
	${ENV}/bin/pip install -r dev-requirements.txt

.PHONY: clean-bootstrap-env
clean-bootstrap-env:
	rm -rf ${ENV}

.PHONY: test
test:
	${TOX} -e py39

.PHONY: lint
lint:
	${TOX} -e lint

.PHONY: build
build: clean
	${ENV}/bin/python setup.py sdist

.PHONY: clean
clean:
	rm -rf dist build

.PHONY: detox
detox: clean
	rm -rf .tox