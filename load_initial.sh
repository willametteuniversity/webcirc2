#!/bin/bash

python manage.py loaddata Building
python manage.py loaddata Location
python manage.py loaddata User
python manage.py loaddata Status
python manage.py loaddata ItemBrand
python manage.py loaddata ItemModel
python manage.py loaddata Collection
python manage.py loaddata Label
python manage.py loaddata InventoryItem
python manage.py loaddata ItemHistory
python manage.py loaddata InstitutionalDepartment
python manage.py laoddata CustomerProfile