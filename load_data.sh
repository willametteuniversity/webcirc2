rm webcirc2/dbwebcirc2.db
~/Envs/wc2/bin/python manage.py syncdb
~/Envs/wc2/bin/python manage.py loaddata User
~/Envs/wc2/bin/python manage.py loaddata Status
#~/Envs/wc2/bin/python manage.py loaddata Reservation
~/Envs/wc2/bin/python manage.py loaddata Location
~/Envs/wc2/bin/python manage.py loaddata Label
~/Envs/wc2/bin/python manage.py loaddata ItemModel
~/Envs/wc2/bin/python manage.py loaddata ItemBrand
~/Envs/wc2/bin/python manage.py loaddata InstitutionalDepartment
~/Envs/wc2/bin/python manage.py loaddata CustomerProfile
~/Envs/wc2/bin/python manage.py loaddata Collection
~/Envs/wc2/bin/python manage.py loaddata Building
~/Envs/wc2/bin/python manage.py loaddata ActionType
#~/Envs/wc2/bin/python manage.py loaddata Action
~/Envs/wc2/bin/python manage.py loaddata NonInventoryItem
~/Envs/wc2/bin/python manage.py loaddata ConsumableItem
~/Envs/wc2/bin/python manage.py loaddata InventoryItem
~/Envs/wc2/bin/python manage.py loaddata ItemHistory
