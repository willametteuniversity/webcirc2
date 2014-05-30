rm webcirc2/dbwebcirc2.db
python manage.py syncdb
python manage.py loaddata User
python manage.py loaddata Status
python manage.py loaddata Reservation
python manage.py loaddata Location
python manage.py loaddata Label
python manage.py loaddata ItemModel
python manage.py loaddata InventoryItem
python manage.py loaddata ItemHistory
python manage.py loaddata ItemBrand
python manage.py loaddata InstitutionalDepartment
python manage.py loaddata CustomerProfile
python manage.py loaddata Collection
python manage.py loaddata Building
python manage.py loaddata ActionType
python manage.py loaddata Action
