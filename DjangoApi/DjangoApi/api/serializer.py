from rest_framework import serializers
from .models import Ingredient
from .models import Cuisine

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'