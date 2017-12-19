## Django Rest Framework (With Models)
* Using python 3.5
* This directory is in contrast to the modellessdrf directory,
as here, models are used
* This directory demonstrates the simplicity of the 
Django Rest Framework (DRF)


### Local Development
#### Working through commands to demonstrate the REST API, GET and POST, locally

```
# test logging before going into virtualenv

python myapp/random_pick.py
INFO:random_pick:30:Random result: 60
INFO:random_pick:32:Is the result divisible by 2 (0=yes, 1=no): 0
INFO:random_pick:40:result: {u'random_result': 60, u'success': u'Pass'}

# activate virtural env

source ~/.virtualenvs/modeldrf35/bin/activate
export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64

python manage.py makemigrations
python manage.py migrate

# start runserver in background
python manage.py runserver &


# explore api, looking for redirects(302) and validation errors and success (200, 201)

http http://127.0.0.1:8000
    HTTP/1.1 302 Found
    Location: /api/



http http://127.0.0.1:8000/api/
    HTTP/1.1 200 OK
    Allow: GET, HEAD, OPTIONS

    {
        "random-picker": "http://127.0.0.1:8000/api/random-picker/"
    }


http http://127.0.0.1:8000/api/random-picker/
    HTTP/1.1 200 OK
    Allow: HEAD, OPTIONS, POST, GET

    []


http http://127.0.0.1:8000/api/random-picker/ start=2 end=200
    HTTP/1.1 201 Created

    {
        "end": 200,
        "id": 1,
        "result": 113,
        "start": 2,
        "status": "Fail"
        "url": "http://127.0.0.1:8000/api/random-picker/1/"
    }


http http://127.0.0.1:8000/api/random-picker/ start=2 end=200
    HTTP/1.1 201 Created

    {
        "end": 200,
        "id": 2,
        "result": 37,
        "start": 2,
        "status": "Fail"
        "url": "http://127.0.0.1:8000/api/random-picker/2/"
    }


http http://127.0.0.1:8000/api/random-picker/
    HTTP/1.1 200 OK

    [
        {
            "end": 200,
            "id": 1,
            "result": 113,
            "start": 2,
            "status": "Fail"
            "url": "http://127.0.0.1:8000/api/random-picker/1/"
        },
        {
            "end": 200,
            "id": 2,
            "result": 37,
            "status": "Fail"
            "start": 2,
            "url": "http://127.0.0.1:8000/api/random-picker/2/"
        }
    ]
    

http http://127.0.0.1:8000/api/random-picker/2/
    HTTP/1.1 200 OK
    
    {
        "end": 200,
        "id": 2,
        "result": 37,
        "start": 2,
        "status": "Fail"
        "url": "http://127.0.0.1:8000/api/random-picker/2/"
    }

```

### Deploying on Openshift (OSP)
* There is no need to be in the python virtual environment to deploy on OSP
* However being in the virtual environment allows one to use httpie,
instead of curl
* One can also deploy this without the openshift secret below:
    * use the template `openshift/templates/restapi_build_no_git_sshsecret.yaml` 
    * use the https value in the parameter file `typical_openshift_param_file.txt`

```
oc new-project myuserid-drf-model
oc secrets new-sshauth sshsecret --ssh-privatekey=$HOME/.ssh/id_rsa_git
oc secret add serviceaccount/builder secrets/sshsecret

oc new-app --param-file typical_openshift_param_file.txt -f openshift/templates/restapi_build.yaml

oc get pods
oc logs -f bc/drf-model
oc get pods -w
oc logs -f dc/drf-model

~/git_repos/oc get routes

    NAME              HOST/PORT                                      PATH      SERVICES          PORT      TERMINATION     WILDCARD
    drf-model     modeldrf.fqdn ... 3 more             drf-model     <all>     edge/Redirect   None

curl -k -I https://modeldrf.fqdn
    HTTP/1.1 302 Found
    Location: /api/

curl -k -s https://modeldrf.fqdn/api/
    {"random-picker":"https://modeldrf.fqdn/api/random-picker/"}

curl -k -s https://modeldrf.fqdn/api/random-picker/
    []

# Leverage HTTPie python module
source ~/.virtualenvs/modeldrf35/bin/activate
export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64

(modeldrf35) http https://modeldrf.fqdn
    HTTP/1.1 302 Found
    Location: /api/

(modeldrf35) http https://modeldrf.fqdn/api/
    HTTP/1.1 200 OK
    {
        "random-picker": "https://modeldrf.fqdn/api/random-picker/"
    }

(modeldrf35) http https://modeldrf.fqdn/api/random-picker/
    HTTP/1.1 200 OK
    Allow: HEAD, OPTIONS, POST, GET
    Content-Type: application/json
    []

(modeldrf35) http https://modeldrf.fqdn/api/random-picker/ start=100 end=200
    HTTP/1.1 201 Created
    
    {
        "end": 200,
        "id": 1,
        "result": 121,
        "start": 100,
        "status": "Fail"
        "url": "https://modeldrf.fqdn/api/random-picker/1/"
    }
    
(modeldrf35) http https://modeldrf.fqdn/api/random-picker/ start=200 end=300
    HTTP/1.1 201 Created
    
    {
        "end": 300,
        "id": 2,
        "result": 274,
        "start": 200,
        "status": "Pass"
        "url": "https://modeldrf.fqdn/api/random-picker/2/"
    }
    
(modeldrf35) http https://modeldrf.fqdn/api/random-picker/
    HTTP/1.1 200 OK
    
    [
        {
            "end": 200,
            "id": 1,
            "result": 121,
            "start": 100,
            "status": "Fail"
            "url": "https://modeldrf.fqdn/api/random-picker/1/"
        },
        {
            "end": 300,
            "id": 2,
            "result": 274,
            "start": 200,
            "status": "Pass"
            "url": "https://modeldrf.fqdn/api/random-picker/2/"
        }
    ]

```

### Notes on running postgresql locally for development
* When a database besides sqlite3 is used, here is an example of 
spining up a postregsql for devlopement.  When the project is 
spun up in Openshift, this happnes automatically

```
source postgres_local_dev_env.sh

# Create postgresql running instance with this command
oc new-app -p POSTGRESQL_USER=${DATABASE_USER} \
           -p POSTGRESQL_PASSWORD=${DATABASE_PASSWORD} \
           -p POSTGRESQL_DATABASE=${DATABASE_NAME} \
           -f openshift/templates/postgresql-ephemeral.yaml

oc port-forward <pod> 5432

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# Then curl or httpie the API endpoint


# Cleaning up PostgreSQL project
oc delete all --all
oc delete secrets <secretname>
```

### Deploying on Openshift using Postgresql
Use this template

```

oc new-app --param-file typical_openshift_param_file.txt -f openshift/templates/restapi_build_postgresql.yaml

```

### References

* http://www.django-rest-framework.org/
* http://www.cdrf.co/


