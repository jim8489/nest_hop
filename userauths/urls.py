from django.urls import path
from userauths import views

urlpatterns = [
    path("sign-up/", views.register_view, name= "signup"),
    path("sign-in/", views.login_view, name= "login"),
    path("sign-out/", views.logout_view, name= "logout"),
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate_account'),

]