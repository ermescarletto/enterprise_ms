from django.urls import path, include
from .views import *

app_name = 'cms'
urlpatterns = [
    path("", Index.as_view(), name='index'),
    path("upload/", process_json, name="upload_json"),

]
