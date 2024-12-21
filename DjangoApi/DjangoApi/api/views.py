from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Ingredient , Cuisine
from .serializer import IngredientSerializer , CuisineSerializer

@api_view(['GET'])
def get_ingredients(request):
    ingredients  = Ingredient.objects.all()
    serializer = IngredientSerializer(ingredients,many= True)
    return Response(serializer.data)


@api_view(['POST'])
def create_ingredient(request):
    serializer = IngredientSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def ingredient_details(request , pk):
    try:
        ingredient = Ingredient.objects.get(pk=pk)
    except Ingredient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = IngredientSerializer(ingredient , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        ingredient.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)
    



@api_view(['GET'])
def get_cuisines(request):
    cuisines  = Cuisine.objects.all()
    serializer = CuisineSerializer(cuisines,many= True)
    return Response(serializer.data)


@api_view(['POST'])
def create_cuisine(request):
    serializer = CuisineSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def cuisine_details(request , pk):
    try:
        cuisine = Cuisine.objects.get(pk=pk)
    except Cuisine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CuisineSerializer(cuisine)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = CuisineSerializer(cuisine , data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        cuisine.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    

# Create your views here.
