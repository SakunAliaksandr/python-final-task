from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
from .views import redirect_view, todo, category

urlpatterns = [
    path('', views.index, name='index'),

    url(r'$^', redirect_view),
    url(r'^todo/$', todo, name="TodoList"),
    url(r'^category/', category, name="Category"),
    # path('<int:todo_id>/', views.detail, name='detail'),
    url(r'^todos/$', views.TodoListView.as_view(), name='todos'),

    url(r'^todo/(?P<pk>\d+)$', views.TodoDetailView.as_view(), name='todo-detail'),
    url(r'^todo/(?P<pk>\d+)/add_message$', views.add_message, name='add_message'),

]