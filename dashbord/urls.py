from django.urls import include,path
from .import views

urlpatterns = [
    path('',views.dashbords,name='dashbords'),
    path('create-user/',views.create,name='create'),
    path('edit/<int:user_id>',views.edit,name='edit'),
    path('delete/<int:user_id>',views.delete,name='delete'),
    path('search/',views.search,name='search'),
]
