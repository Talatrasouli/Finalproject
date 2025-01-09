from rest_framework import serializers
from ads.models import Category,Users,City,Ad

class CategorySerializer(serializers.ModelSerializer):
   

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug',
            'parent',
        ]

class UserSerializer(serializers.ModelSerializer):
       class Meta:
        model=Users
        fields=[
            'id',
            'email',
            'first_name',
            'last_name',
        ]


class CitySerializer(serializers.ModelSerializer):
   class Meta:
        model=City
        fields=[
            'name',
        ]



class AdListSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    owner=UserSerializer(read_only=True)
    city=CitySerializer(read_only=True)
    
    class Meta:
        model=Ad
        fields=[
            'id',
            'owner',
            'category', 
            'title',
            'slug',
            'overview',
            'publish',
            'created_at',
            'updated',
            'image',
            'city',
            'status', 
            
        ]




class AdDetailSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    owner=UserSerializer(read_only=True)
    city=CitySerializer(read_only=True)
    
    class Meta:
        model=Ad
        fields=[
            'id',
            'owner',
            'category', 
            'title',
            'slug',
            'overview',
            'publish',
            'created_at',
            'updated',
            'description',
            'price',
            'image',
            'city',
            'status',
            
        ]