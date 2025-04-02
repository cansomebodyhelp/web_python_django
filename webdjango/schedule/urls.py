from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trains/', views.create_train, name='create_train'),
    path('trains/<int:train_id>/', views.delete_train, name='delete_train'),
    path('trains/list/', views.get_trains, name='get_trains'),
    path('stations/', views.create_station, name='create_station'),
    path('stations/<int:station_id>/', views.delete_station, name='delete_station'),
    path('stations/list/', views.get_stations, name='get_stations'),
    path('records/', views.create_record, name='create_record'),
    path('records/<str:record_id>/', views.delete_record, name='delete_record'),
]