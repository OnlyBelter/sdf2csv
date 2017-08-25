# sdf2csv
A simple Django project, this project can convert a file's format from sdf to csv online.


# Dependencies
I use Python 2.7 (Python 3.x may also ok, didn't test) and Django 1.10

You also need:

`pandas`

# Basic idea
I upload a `.sdf` file and convert it to a `.csv` file, then I count how many lines in the result and give a link to download this `.csv` file.

The result file is stored on server file system(backend), the download url looks like: 

### `http://localhost:8000/static/downloads/Aug-18-2017_1523/result2.csv`

# How to
1. Create a Django Project and App

```
django-admin startproject sdf2csv

cd sdf2csv

python manage.py startapp parseSDF
```

2. Create a file `forms.py` in dir `sdf2csv/parseSDF` to define a form that is needed by input UI

3. Modify file `settings.py`

- add `'DIRS': [os.path.join(BASE_DIR, 'parseSDF', 'templates')],` 
for `TEMPLATES` so we can create templates in this directory

- add following sentences to set static files dir
```
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'sdf2csv', 'static', 'static_root')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'sdf2csv', 'static', 'static_dirs'),
    # https://docs.djangoproject.com/en/1.11/ref/settings/#staticfiles-dirs
    ('downloads', 'D:/downloads'),  # <-- you can change here to set a different dir to store result file
]

```

Also create a folder `static` in dir `sdf2csv/sdf2csv`, and two subfolders `static_dirs` & `static_root` in `static`.

4. Create a folder `templates` in dir `parseSDF`, 
then we create two `.html` files in this folder

- index.html
- result.html

5. Set url in file `urls.py`

```
from django.conf.urls import url
from parseSDF import views


urlpatterns = [
    url(r'^(?i)home/$', views.parse_sdf),
    url(r'^(?i)result/$', views.result),
]

```

6. Write code in file `parseSDF/views.py`, then it can work

7. Deployment static files

`django.contrib.staticfiles` provides a convenience management command for gathering static files in a single directory so you can serve them easily.

Run the collectstatic management command:

`python manage.py collectstatic`

This will copy all files from your static folders into the `STATIC_ROOT` directory.

# Run it locally
Run `python manage.py runserver 0.0.0.0:8000`

Then you can see it from `http://localhost:8024/home/`

You may also want to change the path where the result file be stored, you need to change two places:
 
- In file `settings.py` change `STATICFILES_DIRS`
- Also need to change `DOWNLOAD_ROOT_DIR`'s value in file `parseSDF/public_function.py`. If you set `('downloads', '/opt/webfiles/common/downloads')`, the `DOWNLOAD_ROOT_DIR` should be `/opt/webfiles/common`

# Test data
You can download `.sdf` file from [here](https://github.com/OnlyBelter/some_code/tree/master/data)
