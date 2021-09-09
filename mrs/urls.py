
from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('' , views.main_view , name= 'main_page') ,
    path('show_movies/' , views.search_view , name = 'search_result') ,
    path ('api_result' , views.api , name = 'api') ,
    path('test/' , views.test , name = 'test'),
    path('reviews/' , views.reviews , name = 'reviews')


]
