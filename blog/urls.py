from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('users/', views.user_list, name='user_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<str:category_name>/', views.category_detail, name='category_detail'),
    path('post/<int:post_id>/add_category/', views.add_category_to_post, name='add_category_to_post'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
]