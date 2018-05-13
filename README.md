# DinDin API
### REST API for DinDIn storage

[![Build Status](https://travis-ci.org/flyiniggle/DinDinAPI.svg?branch=master)](https://travis-ci.org/flyiniggle/DinDinAPI)
[![Coverage Status](https://coveralls.io/repos/github/flyiniggle/DinDinAPI/badge.svg?branch=master)](https://coveralls.io/github/flyiniggle/DinDinAPI?branch=master)

## Dev Setup
```buildoutcfg
python manage.py migrate
demodata.bat
python manage.py runserver
```

## Generating Test Data
### dumping new fixtures from a database
```buildoutcfg
python manage.py dumpdata meals --format=json --indent=4 > ./meals/fixtures/mealsdump.json
python manage.py dumpdata auth --format=json --indent=4 > ./meals/fixtures/authdump.json
python manage.py dumpdata authtoken --format=json --indent=4 > ./meals/fixtures/tokendump.json
```

## Running tests
```buildoutcfg
python manage.py test --pattern="*test.py"
```

## Running tests with coverage
```buildoutcfg
coverage run manage.py test --pattern="*test.py"
coverage report -m
```