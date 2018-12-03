lint:
	flake8 .
	pylint crawl config.py models.py fetch.py web.py export.pyS

release:
	pyinstaller -F fetch.py
	pyinstaller -F web.py
	cp -r templates ./dist/
	mkdir ./dist/static
	cp -r ./static/themes ./static/*.js ./static/*.css ./static/*.gif ./dist/static/
	mkdir ./dist/log

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

	rm -fr log/*.log

	find . -name '*.spec' -exec rm -fr {} +
	rm -fr build
	rm -fr dist
