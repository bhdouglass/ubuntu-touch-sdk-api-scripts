#!/usr/bin/make
PYTHON := /usr/bin/env python
SOURCE_DIR := $(PWD)

update-charm: collectstatic
	@echo "Updating charm"
	if [ $(DATABASE_URL) ]; then $(MAKE) initdb; fi

initdb: syncdb
	@echo "Initializing database"
	@python manage.py initdb --settings charm_settings

syncdb:
	@echo "Syncing database"
	@python manage.py syncdb --noinput --migrate --settings charm_settings

collectstatic: collectstatic.done
collectstatic.done:
	@echo "Collecting static files"
	@python manage.py collectstatic --noinput --settings charm_settings
	@touch collectstatic.done

update-pip-cache:
	rm -rf pip-cache
	bzr branch lp:~mhall119/developer-ubuntu-com/dependencies pip-cache
	pip install --exists-action=w --download pip-cache/ -r requirements.txt
	bzr commit pip-cache/ -m 'automatically updated devportal requirements'
	bzr push --directory pip-cache lp:~mhall119/developer-ubuntu-com/dependencies
	bzr revno pip-cache > pip-cache-revno.txt
	rm -rf pip-cache
	@echo "** Remember to commit pip-cache-revno.txt"

pip-cache:
	bzr branch -r `cat pip-cache-revno.txt` lp:~mhall119/developer-ubuntu-com/dependencies pip-cache

tarball: pip-cache
	cd ..; tar -C $(SOURCE_DIR) --exclude-vcs -czf developer_portal.tar.gz .
