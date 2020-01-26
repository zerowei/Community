from django.urls import path, include
from .views import ShowProfile, UpdateProfile
from django.conf import settings
from django.conf.urls.static import static

app_name = 'profile'
urlpatterns = [
    path('user/', include(([
        path('<int:pk>/profile', ShowProfile.as_view(), name='ShowProfile'),
        path('<int:pk>/edit', UpdateProfile.as_view(), name='UpdateProfile'),
    ])))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
