## Simple examples: Django Rest Framework on Openshift 3.6
* There are two approaches here, using, or not using, models.
* See the two different directories for these two approaches.
* This Readme applies to both, setting up the python virtual environment,
and logging.
* For this project, using python 3.x is encouraged, over python 2.7

## Locally, on RHEL/Centos 7.x

### Setting up virtualenv for working locally
#### Python 2.7

```
shell> virtualenv $HOME/.virtualenvs/modellessdrf
shell> export PROXY=ip:port
(modellessdrf) shell> source $HOME/.virtualenvs/modellessdrf/bin/activate
(modellessdrf) shell> pip --proxy $PROXY install pip --upgrade

# Note: django 2.0 not compatible with python 2.7
(modellessdrf) shell> curl -sk -x $PROXY https://pypi.python.org/simple/django/ | awk -F"[<>]" '{print $3}' |egrep 'tar.gz$' |sort -nr 
....
Django-1.11.8.tar.gz
...

(modellessdrf) shell> pip --proxy $PROXY install django==1.11.8 djangorestframework httpie
(modellessdrf) shell> echo "django==1.11.8" > requirements_py27.txt
(modellessdrf) shell> echo "djangorestframework==3.7.3" >> requirements_py27.txt
(modellessdrf) shell> echo "httpie==0.9.9" >> requirements_py27.txt


(modellessdrf) shell> deactivate

```

#### Python 3.x
* Ask your system adminsistrator to install python 3.x (latest)
from the SCL, Software Collections Library.

```
shell> scl --list
rh-python34
rh-python35

shell> scl enable rh-python35 bash
shell> python
Python 3.5.1 (default, Sep 15 2016, 08:30:32)

shell> virtualenv-3.5 ~/.virtualenvs/modellessdrf35

# Get out of the SCL shell
shell> exit
exit

# Verify we're out
shell> python --version
Python 2.7.5

# Activate python 3.5 in a more sane way than going through SCL
shell> source ~/.virtualenvs/modellessdrf35/bin/activate

(modellessdrf35)shell> export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64
(modellessdrf35)shell> python --version
Python 3.5.1

(modellessdrf35)shell> pip --proxy $PROXY install pip --upgrade
(modellessdrf35)shell> pip --proxy $PROXY install django djangorestframework httpie django-cors-headers gunicorn
(modellessdrf35)shell> echo 'django==2.0
> djangorestframework==3.7.3
> django-cors-headers==2.1.0
> gunicorn==19.7.1
> httpie==0.9.9' > requirements.txt
```

(modellessdrf35)shell> deactivate

## In General all of the examples in this repo will be using python 3.5
```
shell> source ~/.virtualenvs/modellessdrf35/bin/activate
(modellessdrf35)shell> export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64
```

### Encouraging using python/django logging, not print statements

#### Example of logging: see ` modellessdrf/myapp/random_pick.py`
This example actually checks to see if django logging is available.
This check is only needed for files that may or may not be used with django.

* without django 

```
# and with python 2.7, without django
shell> python myapp/random_pick.py
INFO:random_pick:30:Random result: 47
INFO:random_pick:32:Is the result divisible by 2 (0=yes, 1=no): 1
INFO:random_pick:40:result: {u'random_result': 47, u'success': u'Fail'}

# and with python 3.5, without django
shell> scl enable rh-python35 bash
shell> python myapp/random_pick.py
INFO:random_pick:30:Random result: 31
INFO:random_pick:32:Is the result divisible by 2 (0=yes, 1=no): 1
INFO:random_pick:40:result: {'random_result': 31, 'success': 'Fail'}
shell> exit
exit
```

* with django, python 3.5
```
(modellessdrf35)shell> python manage.py shell
>>> from myapp import random_pick
>>> dir(random_pick)
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'get_rand_int', 'logger', 'logging', 'randint', 'settings', 'unicode_literals']
>>> random_pick.get_rand_int(1,1000)
INFO:random_pick:30:Random result: 6
INFO:random_pick:32:Is the result divisible by 2 (0=yes, 1=no): 0
{'random_result': 6, 'success': 'Pass'}
>>>
```
