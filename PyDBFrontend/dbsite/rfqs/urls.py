from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('upload/', views.rfq_upload, name='rfq_upload'),
]