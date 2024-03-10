from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= 'home'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name= 'profile'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name= "logout"),
    path('register/', views.register_user, name= "register"),
    path('profile/update', views.update_user, name= "update_user"),
    path('post/<int:pk>/like', views.post_like,  name="post_like"),
    path('post/<int:pk>/show', views.post_show,  name="post_show"),
    path('post/<int:pk>/delete', views.post_delete, name='post_delete'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('comment/<int:pk>', views.comment, name='comment'),
    path('comment/<int:pk>/delete', views.comment_delete, name='comment_delete'),
]
