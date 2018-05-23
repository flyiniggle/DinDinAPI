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
python manage.py dumpdata --format=json --indent=4 > ./meals/fixtures/dump.json
python manage.py dumpdata --format=json --indent=4 > ./accounts/fixtures/dump.json
```

## Running tests
```buildoutcfg
python manage.py test --pattern="*Test.py"
```

## Running tests with coverage
```buildoutcfg
coverage run manage.py test --pattern="*Test.py"
coverage report -m
```

## Demo Data

### Users

|User Name|First Name|Last Name|Password|Email|Super User|Staff|Owned Meals|Meals From Other Users|Meals From Other Users Pending Collaboration|Meals Pending Acceptance by Other Users|
|--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |
|admin|Admin|McAdminson|testing123|admin@dindin.com|true|true|4|2|3|2|
|test1|Jamal|Herrington|testing123|jamal@dindin.com|false|false|4|1|3|3|
|test2|Demitri|Sharoon|testing123|ds@dindin.com|false|false|1|0|1|2|
|test3|||testing123||false|false|0|0|0|