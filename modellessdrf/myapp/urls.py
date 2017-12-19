from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()  
router.register(r'random-picker', views.RandomPickerViewSet, base_name='random_picker')

# vim: ai et ts=4 sw=4 sts=4 nu ru
