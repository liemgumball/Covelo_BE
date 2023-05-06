# Covelo_BE

## Installation

Create a new virtual environment using the following command:

```bash
python -m venv env
```

Activate the virtual environment by running the activate script. Run the following command:

```bash
source env\bin\activate
```

Once the virtual environment is activated, you can install the packages listed in the requirements.txt file using the following command:

```bash
pip install -r requirements.txt
```

Update the requirements.txt by:
```bash
pip freeze > requirements.txt
```

Customize database connection in **settings.py**:

```python
DATABASES = {
    'default': {
    }
}
```

Migrate database:

```bash
cd covelo
python manage.py migrate
```

Run the server:

```bash
python manage.py runserver
```

## Add mock data throught admin view

Create a super user:

```bash
cd covelo
python manage.py createsuperuser
```

Access the admin site:

```bash
http://localhost:8000/admin/
```