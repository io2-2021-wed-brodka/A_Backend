from django.urls import path

from .views import bikes_list, bikes_detail

urlpatterns = [
    path('bikes/', bikes_list, name = 'bikes_list'),
    path('bikes/<int:pk>', bikes_detail, name = 'bikes_detail')
]
