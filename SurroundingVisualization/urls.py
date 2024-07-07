from django.contrib import admin
from django.urls import include, path
from mapCreation.consumers import CarMappingConsumer
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('car_mapping/', include('mapCreation.urls')),
]

urlpatterns += staticfiles_urlpatterns()

websocket_urlpatterns = [
    path('ws/car_mapping/<int:room_id>/', CarMappingConsumer.as_asgi()),
]

