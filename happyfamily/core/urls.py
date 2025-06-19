from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

urlpatterns += [
    path('update_student/<str:id>/', views.update_student),
    path('delete_student/<str:id>/', views.delete_student),
    path('users/', views.user_list, name='user_list'),
    path('update_user/<str:id>/', views.update_user),
    path('delete_user/<str:id>/', views.delete_user),
    path('add_user/', views.add_user, name='add_user'),
    path('add_student/', views.add_student, name='add_student'),
]

