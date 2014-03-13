#!/bin/bash

python manage.py loaddata Building
python manage.py loaddata Location
python manage.py loaddata User
python manage.py loaddata Status
python manage.py loaddata ItemBrand
python manage.py loaddata ItemModel
python manage.py loaddata Collection
