from django.urls import path
from . import views


app_name = 'pillrecognition'
urlpatterns = [
    path('', views.pill_recognition_view, name='index'),
    path('results/', views.results_view, name='results')
]
