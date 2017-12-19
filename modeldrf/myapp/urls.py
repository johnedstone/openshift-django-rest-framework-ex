from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()  

# Adding base_name here throws an error trying to return the 'url' in the serializer
# router.register(r'random-picker', views.RandomPickerViewSet, base_name='random_picker')
router.register(r'random-picker', views.RandomPickerViewSet)

# vim: ai et ts=4 sw=4 sts=4 nu ru
