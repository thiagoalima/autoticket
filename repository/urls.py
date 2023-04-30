from django.urls import path

from . import views

app_name = 'repository'

urlpatterns = [

    # Repository urls
    path('repo/',views.RepoListView.as_view(), name='repo'),
    path('repo/<pk>',views.RepoDetailView.as_view(), name='repo_detail'),
    path('repo/add/',views.RepoCreateView.as_view(), name='repo_add'),
    path('repo/edit/<pk>',views.RepoUpdateView.as_view(), name='repo_edit'),
    path('repo/del/<pk>',views.RepoDeleteView.as_view(), name='repo_del'),

    # Playbook urls
    path('playbook/<pk>',views.PlaybookDetailView.as_view(), name='playbook_detail'),
    path('playbook/host/add/<pk>',views.AddHostView.as_view(), name='host_add'),
    path('playbook/host/del/<pk>',views.HostDeleteView.as_view(), name='host_del'),
    path('playbook/host/join/<pk>',views.JoinGroupHostView.as_view(), name='host_join_group'),
    path('playbook/host/vars/<pk>',views.HostVarsDetailView.as_view(), name='host_vars_detail'),
    path('playbook/group/add/<pk>',views.AddGroupView.as_view(), name='group_add'),
    path('playbook/group/del/<pk>',views.GroupDeleteView.as_view(), name='group_del'),
    path('playbook/group/vars/<pk>',views.GroupVarsDetailView.as_view(), name='group_vars_detail'),
    path('playbook/file/add/<pk>',views.AddFileView.as_view(), name='Playbookfile_add'),
    path('playbook/play/host/add/<pk>',views.AddHostPlaybookView.as_view(), name='playbook_host_add'),
    path('playbook/play/vars/add/<pk>',views.AddVarsPlaybookView.as_view(), name='playbook_vars_add'),
    path('playbook/play/task/add/<pk>',views.AddTaskPlaybookView.as_view(), name='playbook_task_add'),
    path('playbook/play/tasks/<pk>',views.TaskDetailView.as_view(), name='playbook_task_detail'),
]   

