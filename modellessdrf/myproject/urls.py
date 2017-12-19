from django.conf.urls import url, include  
from django.http import HttpResponse
from django.shortcuts import redirect


from myapp.urls import router as myapp_router

urlpatterns = [  
    url(r'^$', lambda x: redirect('/api/', permanent=False), name='home'),
    url(r'^api/', include(myapp_router.urls)),

    url(r'^liveness/', lambda request:HttpResponse(status=200)),
    url(r'^readiness/', lambda request:HttpResponse(status=200)),
]

# vim: ai et ts=4 sw=4 sts=4 nu ru
