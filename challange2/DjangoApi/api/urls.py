from django.urls import path
from .views import get_ingredients
from .views import create_ingredient
from .views import ingredient_details
from .views import get_cuisines
from .views import create_cuisine
from .views import cuisine_details

urlpatterns = [
    path('ingredients/',get_ingredients , name ='get_ingredients'),
    path('ingredients/create',create_ingredient , name ='create_ingredient'),
    path('ingredients/<int:pk>',ingredient_details , name ='ingredient_details'),

    path('cuisines/',get_cuisines , name ='get_cuisines'),
    path('cuisines/create',create_cuisine , name ='create_cuisine'),
    path('cuisines/<int:pk>',cuisine_details , name ='cuisine_details')

]