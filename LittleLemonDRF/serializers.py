from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Category, MenuItem, Cart, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ("id", "title", "price", "featured", "category")


class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "user", "menuitem", "quantity", "unit_price", "price")


class OrderSerializer(serializers.ModelSerializer):
    cart_items = CartSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ("id", "user", "cart_items", "status", "delivery_crew")


class DeliveryCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")
