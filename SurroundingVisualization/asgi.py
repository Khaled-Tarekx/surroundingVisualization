import os
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()
from dotenv import load_dotenv
from channels.routing import ProtocolTypeRouter, URLRouter
from mapCreation.routing import websocket_urlpatterns

load_dotenv()

if os.environ.get('DEBUG') == 'True':
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    static_urls = staticfiles_urlpatterns()
    application = ProtocolTypeRouter({
        'http': get_asgi_application(),
        'websocket': URLRouter(
            websocket_urlpatterns
        ),
        'static': static_urls,
    })
