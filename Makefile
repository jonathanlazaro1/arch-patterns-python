pip-compile:
	pip-compile --generate-hashes requirements.in --output-file requirements.txt
	pip-compile --generate-hashes requirements-dev.in --output-file requirements-dev.txt

pip-upgrade:
	pip-compile --upgrade

setup:
	pip-sync requirements.txt

dev-setup:
	pip-sync requirements-dev.txt requirements.txt

test:
	pytest tests/unit