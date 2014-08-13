rm webcirc2/dbwebcirc2.db
~/venvwebcirc2/bin/python manage.py syncdb
~/venvwebcirc2/bin/python manage.py loaddata User
~/venvwebcirc2/bin/python manage.py loaddata Status
#~/venvwebcirc2/bin/python manage.py loaddata Reservation
~/venvwebcirc2/bin/python manage.py loaddata Location
~/venvwebcirc2/bin/python manage.py loaddata Label
~/venvwebcirc2/bin/python manage.py loaddata ItemModel
~/venvwebcirc2/bin/python manage.py loaddata ItemBrand
~/venvwebcirc2/bin/python manage.py loaddata InstitutionalDepartment
~/venvwebcirc2/bin/python manage.py loaddata CustomerProfile
~/venvwebcirc2/bin/python manage.py loaddata Collection
~/venvwebcirc2/bin/python manage.py loaddata Building
~/venvwebcirc2/bin/python manage.py loaddata ActionType
#~/venvwebcirc2/bin/python manage.py loaddata Action
~/venvwebcirc2/bin/python manage.py loaddata NonInventoryItem
~/venvwebcirc2/bin/python manage.py loaddata ConsumableItem
~/venvwebcirc2/bin/python manage.py loaddata InventoryItem
~/venvwebcirc2/bin/python manage.py loaddata ItemHistory
