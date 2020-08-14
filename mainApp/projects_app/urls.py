from django.urls import path, include
from . import views

# list views ------------------------------------------------------------------------------------
urlpatterns = [
    path("", views.ProjectListView.as_view(), name="projects"),
    path('customers/', views.CustomerListView.as_view(), name="customers"),
    path('domains/', views.DomainListView.as_view(), name="domains"),
    path('objectives/', views.ObjectiveListView.as_view(), name="objectives"),
    # path('projects/', views.ProjectListView.as_view(), name="projects"),
    path('workitems/', views.workitem_list_view, name="workitems"), 
    path('init', views.init),
]


# Customer views ------------------------------------------------------------------------------------
urlpatterns += [
    path('customer/<int:pk>', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('customer/add', views.CustomerCreateView.as_view(), name='customer-add'),
    path('customer/update/<int:pk>', views.CustomerUpdateView.as_view(), name='customer-update'),
    path('customer/delete/<int:pk>', views.CustomerDeleteView.as_view(), name='customer-delete'),
]

# Objective views ------------------------------------------------------------------------------------
urlpatterns += [
    path('objective/<int:pk>', views.ObjectiveDetailView.as_view(), name='objective-detail'),
    path('objective/add', views.ObjectiveCreateView.as_view(), name='objective-add'),
    path('objective/update/<int:pk>', views.ObjectiveUpdateView.as_view(), name='objective-update'),
    path('objective/delete/<int:pk>', views.ObjectiveDeleteView.as_view(), name='objective-delete'),
]

# Domain views ------------------------------------------------------------------------------------
urlpatterns += [
    path('domain/<int:pk>', views.DomainDetailView.as_view(), name='domain-detail'),
    path('domain/add', views.DomainCreateView.as_view(), name='domain-add'),
    path('domain/update/<int:pk>', views.DomainUpdateView.as_view(), name='domain-update'),
    path('domain/delete/<int:pk>', views.DomainDeleteView.as_view(), name='domain-delete'),
]

# Workitem views ------------------------------------------------------------------------------------
urlpatterns += [
    path('workitem/<int:pk>', views.WorkItemDetailView.as_view(), name='workitem-detail'),
    path('workitem/add', views.WorkItemCreateView.as_view(), name='workitem-add'),
    path('workitem/update/<int:pk>', views.WorkItemUpdateView.as_view(), name='workitem-update'),
    path('workitem/delete/<int:pk>', views.WorkItemDeleteView.as_view(), name='workitem-delete'),
]

# Project views ------------------------------------------------------------------------------------
urlpatterns += [
    path('project/add', views.ProjectCreateView.as_view(), name='project-add'),
    path('project/<int:project_id>/', views.project, name='project'),
    path('project/<int:project_id>/<int:workitem_id>', views.project_workitems, name='project-workitems'),
    path('project/addworkitem/<int:pk>', views.project_addworkitem, name="project-update-workitems"),
    path('project/progress/<int:project_id>', views.project_progress, name = "project-progress"),
    path('project/delete/<int:pk>', views.ProjectDeleteView.as_view(), name = "project-delete"),
    path('project/update/<int:pk>/', views.ProjectUpdateView.as_view(), name='project-edit'),
    path('project/<int:project_id>/<int:workitem_id>/<int:message_id>', views.retrieve_file, name='retrieve-file'),
    path('project/adduserpage/<int:pk>/', views.add_user_page, name='project-add-user-page'),
    path('project/adduser/<int:pk>/', views.add_user, name='project-add-user'),
    path('project/removeuser/<int:pk>/<int:uk>/', views.remove_user, name='project-remove-user'),
    path('project/status/<int:pk>', views.ProjectStatusUpdateView.as_view(), name='project-status'),
    path('project/domaintable/<int:pk>/<int:uk>/', views.domain_table, name='project-domain-table'),
    path('project/domaintable/addcolumn/<int:pk>/<int:uk>/', views.add_table_column, name='project-add-column'),
    path('project/domaintable/addrow/<int:pk>/<int:uk>/', views.add_table_row, name='project-add-row'),
]

# Auth views ------------------------------------------------------------------------------------
from django.contrib.auth import views as auth_views
urlpatterns += [
    path('accounts/login/' ,auth_views.LoginView.as_view(), name='login'),
]

# Generate proposal view

urlpatterns += [
    path('project/<int:pk>/genpro/', views.generateProposal, name='genproposal'),
    path('project/<int:pk>/geneng/', views.generateEngagement, name='genengagement')
]
