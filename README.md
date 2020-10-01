# `va_api backend`

### How to setup

Create a virtual environment
```
virtualenv venv
```

Add these environment variables to the file ```/venv/bin/activate```
```
# not necesary when running gunicorn, only debug
export DATABASE=<database connection string>
export USERNAME=<username>
export PASSWORD=<password>
export DB=<database name>
```

Activate the virtual environment
```
source /venv/bin/activate
```

Install all libraries
```
pip3 install -r requirements.txt
```


### How to run

```
gunicorn API:app --bind 0.0.0.0:1024 --timeout 30 --log-level info
```

### Current endpoints
# Returns first document from va_preference
'''
/domain_api/va/max_threshold/
'''

