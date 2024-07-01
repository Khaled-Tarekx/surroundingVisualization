from django.urls import  path
from mapCreation import views

urlpatterns = [
    path('<int:room_id>/', views.car_mapping_visualization, name='car_mapping_visualization'),
]


