from django.urls import path

from .import views


urlpatterns = [
   path("",views.home),
   path("singup/",views.singup),
   path("login/",views.login),
   path("dashboard/",views.dashboard),
   path("logout/",views.logout),
   path("profile_setup/",views.profile_setup)


]
