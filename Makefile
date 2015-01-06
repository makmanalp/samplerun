test:
	. ./env/bin/activate; py.test -v --maxfail=2 samplerun.py
install:
	virtualenv env
	. ./env/bin/activate; pip install -r requirements.txt

