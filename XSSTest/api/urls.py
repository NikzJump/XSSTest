from django.urls import path
from . import views


urlpatterns = [
    path("signup", views.signup),
    path("login", views.login),
    path("transfer", views.transfer_coins),
    path("post_comment/<int:pk>", views.post_comment),
    path("user/<int:pk>", views.get_user_data),
    path("get_names", views.get_user_names)
]
