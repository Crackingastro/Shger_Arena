from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name = "index"), 
    path("pages/<str:id>",views.pages, name = "pages"),
    path("home",views.index, name = "index")
]