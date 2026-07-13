# Define the shell to use
SHELL := bash

# Define variables for reusability
JUPYTER_BOOK = book
VENV = .venv

.PHONY: clean setup start build deploy test

clean:
	deactivate
	rm -rf $(VENV)

setup:
	uv venv --python 3.13
	source $(VENV)/Scripts/activate
	uv python pin 3.13
	uv sync

start:
	export NODE_TLS_REJECT_UNAUTHORIZED=0
	cd $(JUPYTER_BOOK)
	jupyter-book start
	cd ..

build:
	export NODE_TLS_REJECT_UNAUTHORIZED=0
	cd $(JUPYTER_BOOK)
	jupyter-book build --html
	cd ..

deploy:
	cd $(JUPYTER_BOOK)
	jupyter-book init --gh-pages
	cd ..

test:
	pytest tests --maxfail=1 --disable-warnings -q