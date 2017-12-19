## Django Rest Framework Without Models
Using python 3.5


### Local Development
#### Working through commands to demonstrate the REST API, GET and POST, locally

```
# test logging before going into virtualenv

python myapp/random_pick.py
INFO:random_pick:30:Random result: 60
INFO:random_pick:32:Is the result divisible by 2 (0=yes, 1=no): 0
INFO:random_pick:40:result: {u'random_result': 60, u'success': u'Pass'}

# activate virtural env

source ~/.virtualenvs/modellessdrf35/bin/activate
export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64

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
Content-Type: application/json

    [
        {
            "end": 10,
            "result": 8,
            "start": 1,
            "status": "Pass"
        },
        {
            "end": 100,
            "result": 89,
            "start": 10,
            "status": "Fail"
        },
        {
            "end": 1000,
            "result": 898,
            "start": 100,
            "status": "Pass"
        }
    ]

http POST http://127.0.0.1:8000/api/random-picker/
    HTTP/1.1 400 Bad Request
    Content-Length: 71
    
    {
        "end": [
            "This field is required."
        ],
        "start": [
            "This field is required."
        ]
    }

http POST http://127.0.0.1:8000/api/random-picker/ start=20 end=200
    HTTP/1.1 201 Created
    
    {
        "end": 200,
        "result": 97,
        "start": 20,
        "status": "Fail"
    }
    
    http POST http://127.0.0.1:8000/api/random-picker/ start=20 end=200
    HTTP/1.1 201 Created
    
    {
        "end": 200,
        "result": 72,
        "start": 20,
        "status": "Pass"
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
oc new-project myuserid-drf-modelless
oc secrets new-sshauth sshsecret --ssh-privatekey=$HOME/.ssh/id_rsa_git
oc secret add serviceaccount/builder secrets/sshsecret

oc new-app --param-file typical_openshift_param_file.txt -f openshift/templates/restapi_build.yaml

oc get pods
oc logs -f bc/drf-modelless
oc get pods -w
oc logs -f dc/drf-modelless

~/git_repos/oc get routes

    NAME              HOST/PORT                                      PATH      SERVICES          PORT      TERMINATION     WILDCARD
    drf-modelless     modellessdrf.fqdn ... 3 more             drf-modelless     <all>     edge/Redirect   None

curl -k -I https://modellessdrf.fqdn
    HTTP/1.1 302 Found
    Location: /api/

curl -k -s https://modellessdrf.fqdn/api/
    {"random-picker":"https://modellessdrf.fqdn/api/random-picker/"}

curl -k -s https://modellessdrf.fqdn/api/random-picker/
    [{"start":1,"end":10,"result":8,"status":"Pass"},{"start":100,"end":1000,"result":898,"status":"Pass"},{"start":10,"end":100,"result":89,"status":"Fail"}]

# Leverage HTTPie python module
source ~/.virtualenvs/modellessdrf35/bin/activate
export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64

(modellessdrf35)http https://modellessdrf.fqdn
    HTTP/1.1 302 Found
    Location: /api/

(modellessdrf35)http https://modellessdrf.fqdn/api/
    HTTP/1.1 200 OK
    {
        "random-picker": "https://modellessdrf.fqdn/api/random-picker/"
    }

(modellessdrf35)http https://modellessdrf.fqdn/api/random-picker/
    HTTP/1.1 200 OK
    Allow: HEAD, OPTIONS, POST, GET
    Content-Type: application/json
    [
        {
            "end": 10,
            "result": 8,
            "start": 1,
            "status": "Pass"
        },
        ...
]

(modellessdrf35)http https://modellessdrf.fqdn/api/random-picker/ start=100 end=200
    HTTP/1.1 201 Created
    Allow: HEAD, OPTIONS, POST, GET
    {
        "end": 200,
        "result": 110,
        "start": 100,
        "status": "Pass"
    }



```

### References

In order of importance:

* https://medium.com/django-rest-framework/django-rest-framework-viewset-when-you-don-t-have-a-model-335a0490ba6f
* https://github.com/linovia/drf-demo
* http://www.django-rest-framework.org/tutorial/3-class-based-views/
* http://jsatt.com/blog/abusing-django-rest-framework-part-1-non-model-endpoints/
* http://www.cdrf.co/


