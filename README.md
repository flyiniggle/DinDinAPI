# DinDin API
### REST API for DinDIn storage

## Dev Setup
```buildoutcfg
python manage.py migrate
demodata.bat
python manage.py runserver
```

## Generating Test Data
###dumping new fixtures from a database
```buildoutcfg
python manage.py dumpdata meals --format=json --indent=4 > ./meals/fixtures/mealsdump.json
python manage.py dumpdata auth --format=json --indent=4 > ./meals/fixtures/authdump.json
python manage.py dumpdata authtoken --format=json --indent=4 > ./meals/fixtures/tokendump.json
```