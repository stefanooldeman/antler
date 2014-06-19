test: clean
	. ./venv/bin/activate
	python -m unittest discover


clean:
	find . -type f -name "*.pyc" -delete
install:
	easy_install pip
	pip install virtualenv
	virtualenv venv
