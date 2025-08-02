from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('categories/', views.categories, name='categories'),
    path('add-category/', views.add_category, name='add_category'),
    path('reminder-logs/', views.reminder_logs, name='reminder_logs'),
    path('toggle-task/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('send-test-reminder/', views.send_test_reminder, name='send_test_reminder'),
   path('calendar/', views.calendar_view, name='calendar'),
]
