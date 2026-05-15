django 
djangorestframework 
mysqlclient 
bcrypt 
pillow 
django-cors-headers 
djangorestframework-simplejwt 

1. 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

2. DEBUG = False

3. ALLOWED_HOSTS = ["*"]

4. pip install gunicorn

5. pip freeze > requirements.txt

6. 
Procfile - File
web: gunicorn JJPBackend.wsgi

7. Push Project to Github

8. Render -https://dashboard.render.com/

9. 
New +
Web Service
Connect GitHub
Select backend repo

10. 
At bottom of settings.py:
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

Then change settings.py:
SECRET_KEY = os.environ.get("SECRET_KEY")

Environment Variables:
SECRET_KEY = anything_you_want

Build Command
pip install -r requirements.txt 

Start Command
gunicorn JJPBackend.wsgi

11. 
File Changes