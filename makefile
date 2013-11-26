all: magnetron.egg-info

magnetron.egg-info:
	python3 setup.py egg_info

test: all
	python3 setup.py test

clean:
	rm -rf magnetron.egg-info magnetron/__pycache__/
