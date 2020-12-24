from django.urls import path
import socialnetwork.views as views

urlpatterns = [
    path("user/signup/", views.sign_up),
    path('post/create/', views.create_post),
    path('post/<str:post_id>/like', views.trigger_like),
]