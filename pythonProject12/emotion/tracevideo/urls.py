from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "emotion"
urlpatterns = [
    path("", views.index, name="index"),
    path("upload", views.upload_file, name="upload"),
    path("display", views.display, name="display"),
    path('play', views.play_xyz, name="playXYZ")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)