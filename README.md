
# inventory-backend

Ultimate product catalog

![main-structure](https://user-images.githubusercontent.com/20068601/130909583-1ef67788-eefd-4a23-98c1-29b46b87f45a.png)
             
## Settings
                        
All settings are loaded from environment variables or .env file. You may use .env.ci file as default:

```
cp app/.env.ci app/.env
```

## Packages

We are using [pip-tools](https://github.com/jazzband/pip-tools) here.


For first install run:
```
pip install -r requirements.txt 
```

Add new packages only to `requirements.in`.


* to update all dependencies (within specified versions in `requirements.in`)
```
pip-compile -U
```

* to update single package
```
pip-compile -P some-package
```

* to sync packages locally
```
pip-sync
```

## Testing

Make sure you prepared database for tests. You may run `docker-compose up -d` to deploy necessary resources.

```
pytest
```

## Linting
   
Use this ultimate command:

```
isort . && black . && flake8
```
