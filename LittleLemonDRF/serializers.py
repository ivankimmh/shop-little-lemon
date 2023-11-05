from rest_framework import serializers
from django.contrib.auth.models import User, Group
from LittleLemonDRF.models import MenuItem, Booking

# from .models import Category, MenuItem, Cart, Order, OrderItem


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ["id", "title", "slug"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )
        return user


class MenuItemSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ["title", "price", "inventory"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["user", "reservation_date", "reservation_slot"]


# class CartSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), default=serializers.CurrentUserDefault()
#     )

#     def validate(self, attrs):
#         attrs["price"] = attrs["quantity"] * attrs["unit_price"]
#         return attrs

#     class Meta:
#         model = Cart
#         fields = ["user", "menuitem", "unit_price", "quantity", "price"]
#         extra_kwargs = {"price": {"read_only": True}}


# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ["order", "menuitem", "quantity", "price"]


# class OrderSerializer(serializers.ModelSerializer):
#     orderitem = OrderItemSerializer(many=True, read_only=True, source="order")

#     class Meta:
#         model = Order
#         fields = ["id", "user", "delivery_crew", "status", "date", "total", "orderitem"]


class UserSerilializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
