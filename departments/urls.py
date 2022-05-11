from django.urls import path
from . import views

app_name='departments'
urlpatterns = [
    path('', views.BranchListView.as_view(), name='branch_list'),
    path('<slug:slug>/', views.DomainListView.as_view(), name='domain_list'),
    path('<str:branch>/<slug:slug>/', views.ProjectListView.as_view(), name='project_list'),
    path('<str:branch>/<str:slug>/create/', views.ProjectCreateView.as_view(),name='project_create'),
    path('<str:branch>/<str:domain>/<slug:slug>/', views.ProjectDetailView.as_view(),name='project_detail'),
    path('<str:branch>/<str:domain>/<slug:slug>/update/', views.ProjectUpdateView.as_view(),name='project_update'),
    path('<str:branch>/<str:domain>/<slug:slug>/delete/', views.ProjectDeleteView.as_view(),name='project_delete'),

]
