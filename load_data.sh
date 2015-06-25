#!/bin/sh
rm ./webcirc2/dbwebcirc2.db
~/webcirc2/bin/python manage.py syncdb
~/webcirc2/bin/python manage.py loaddata User
~/webcirc2/bin/python manage.py loaddata Status
~/webcirc2/bin/python manage.py loaddata Reservation
~/webcirc2/bin/python manage.py loaddata Location
~/webcirc2/bin/python manage.py loaddata Label
~/webcirc2/bin/python manage.py loaddata ItemModel
~/webcirc2/bin/python manage.py loaddata ItemBrand
~/webcirc2/bin/python manage.py loaddata InstitutionalDepartment
~/webcirc2/bin/python manage.py loaddata CustomerProfile
~/webcirc2/bin/python manage.py loaddata Collection
~/webcirc2/bin/python manage.py loaddata Building
~/webcirc2/bin/python manage.py loaddata ActionType
~/webcirc2/bin/python manage.py loaddata InventoryItem
~/webcirc2/bin/python manage.py loaddata ItemHistory
~/webcirc2/bin/python manage.py loaddata ItemLabel
~/webcirc2/bin/python manage.py loaddata ActionState
~/webcirc2/bin/python manage.py loaddata Action
