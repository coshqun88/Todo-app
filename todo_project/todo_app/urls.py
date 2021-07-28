from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name="index"),
    path('about/', views.about,name="about"),
    path('create/', views.create,name="create"),
    path('delete/<todos_id>', views.delete, name="delete"),
    path('update/<todos_id>', views.update, name="update"),
    path('finish/<todos_id>', views.finish, name="finish"),
    path('no_finish/<todos_id>', views.no_finish, name="no_finish"),
    path('no_finish/<todos_id>', views.no_finish, name="no_finish"),
]