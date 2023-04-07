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
    path('playbook/host/join/<pk>',views.AddHostView.as_view(), name='host_join_group'),

]   

