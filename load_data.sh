#!/bin/sh
rm webcirc2/dbwebcirc2.db
~/webcirc_venv/bin/python manage.py syncdb
~/webcirc_venv/bin/python manage.py loaddata User
~/webcirc_venv/bin/python manage.py loaddata Status
~/webcirc_venv/bin/python manage.py loaddata Reservation
~/webcirc_venv/bin/python manage.py loaddata Location
~/webcirc_venv/bin/python manage.py loaddata Label
~/webcirc_venv/bin/python manage.py loaddata ItemModel
~/webcirc_venv/bin/python manage.py loaddata ItemBrand
~/webcirc_venv/bin/python manage.py loaddata InstitutionalDepartment
~/webcirc_venv/bin/python manage.py loaddata CustomerProfile
~/webcirc_venv/bin/python manage.py loaddata Collection
~/webcirc_venv/bin/python manage.py loaddata Building
~/webcirc_venv/bin/python manage.py loaddata ActionType
~/webcirc_venv/bin/python manage.py loaddata NonInventoryItem
~/webcirc_venv/bin/python manage.py loaddata ConsumableItem
~/webcirc_venv/bin/python manage.py loaddata InventoryItem
~/webcirc_venv/bin/python manage.py loaddata ItemHistory
~/webcirc_venv/bin/python manage.py loaddata ItemLabel
~/webcirc_venv/bin/python manage.py loaddata Action
