from django.urls import path
from .views import index, pass_request_form

urlpatterns = [
    path('', index, name='index'),
    path('pass_request/', pass_request_form, name='pass_request_form'),

]