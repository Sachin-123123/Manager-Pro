from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Dashboard
    path('', login_required(views.dashboard), name='dashboard'),

    # Organization URLs
    path('organizations/', views.OrganizationListView.as_view(), name='organization_list'),
    path('organizations/<int:pk>/', views.OrganizationDetailView.as_view(), name='organization_detail'),
    path('organizations/create/', views.OrganizationCreateView.as_view(), name='organization_create'),
    path('organizations/<int:pk>/update/', views.OrganizationUpdateView.as_view(), name='organization_update'),
    path('organizations/<int:pk>/delete/', views.OrganizationDeleteView.as_view(), name='organization_delete'),
    path('organizations/<int:org_id>/add-member/', views.add_member, name='add_member'),
    path('organizations/<int:org_id>/remove-member/<int:user_id>/', views.remove_member, name='remove_member'),

    # Task URLs
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('organizations/<int:org_id>/tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<int:pk>/complete/', views.mark_task_complete, name='mark_task_complete'),

    # Personal To-Do URLs
    path('personal-todos/', views.PersonalToDoListView.as_view(), name='personal_todo_list'),
    path('personal-todos/create/', views.PersonalToDoCreateView.as_view(), name='personal_todo_create'),
    path('personal-todos/<int:pk>/update/', views.PersonalToDoUpdateView.as_view(), name='personal_todo_update'),
    path('personal-todos/<int:pk>/delete/', views.PersonalToDoDeleteView.as_view(), name='personal_todo_delete'),
    path('personal-todos/<int:pk>/complete/', views.mark_todo_complete, name='mark_todo_complete'),


    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
] 