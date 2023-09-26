from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User, Group
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import (
    UserSerializer,
    GroupSerializer,
    CategorySerializer,
    MenuItemSerializer,
    CartSerializer,
    OrderSerializer,
    DeliveryCrewSerializer,
)
from .permissions import IsManager, IsDeliveryCrew, IsCustomer
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.http import Http404


# User registration and token generation : /api/users
class CreateUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        username = data["username"]
        password = data["password"]
        email = data["email"]

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        hashed_password = make_password(password)

        new_user = User.objects.create(
            username=username, email=email, password=hashed_password
        )

        new_user.save()
        serializer = UserSerializer(new_user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# /token/login/
class TokenLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        username = data["username"]
        password = data["password"]

        if not username or not password:
            return Response(
                {"error": "Username and password must be provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(username=username).first()

        if not user:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        token, created = Token.objects.get_or_create(user=user)

        if created:
            print("New token has been created")

        serializer = UserSerializer(user)

        res = {
            "token": token.key,
            "user": serializer.data,
        }

        return Response(data=res, status=status.HTTP_200_OK)


# /api/users/users/me/
class CurrentUserView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [TokenAuthentication]

    def get(self, request: Request, *args, **kwargs):
        user = request.user
        user_serializer = UserSerializer(user)
        groups = user.groups.all()
        group_serializer = GroupSerializer(groups, many=True)

        res = {
            "user": user_serializer.data,
            "groups": group_serializer.data,
        }
        return Response(data=res, status=status.HTTP_200_OK)


# Menu-items endpoints : /api/menu-items
class MenuItemListView(APIView):
    permission_classes = [IsCustomer | IsDeliveryCrew | IsManager]

    def get(self, request: Request, *args, **kwargs):
        if any(isinstance(request.user, role) for role in [IsCustomer, IsDeliveryCrew]):
            itmes = MenuItem.objects.all()
            serializer = MenuItemSerializer(itmes, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif isinstance(request.user, IsManager):
            items = MenuItem.objects.all()
            serializer = MenuItemSerializer(items, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)

    def post(self, request: Request, *args, **kwargs):
        if isinstance(request.user, IsManager):
            serializer = MenuItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                data = {
                    "Message": "Unauthorized access",
                }
                return Response(data=data, status=status.HTTP_403_FORBIDDEN)


# /api/menu-items/{menuItem}
class SingleMenuItemView(APIView):
    permission_classes = [IsCustomer | IsDeliveryCrew | IsManager]

    def get_menu_item(self, kwargs):
        menu_item_id = kwargs.get("menuItem")
        return get_object_or_404(MenuItem, id=menu_item_id)

    def get(self, request: Request, *args, **kwargs):
        menu_item = self.get_menu_item(kwargs)
        serializer = MenuItemSerializer(menu_item)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsManager):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        menu_item = self.get_menu_item(kwargs)
        serializer = MenuItemSerializer(menu_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsManager):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        menu_item = self.get_menu_item(kwargs)
        serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsManager):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        menu_itme = self.get_menu_item(kwargs)
        menu_itme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# User group management : /api/groups/manager/users
class ManagerUsersView(APIView):
    permission_classes = [IsManager]

    def get(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsManager):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        manager_group = Group.objects.get(name="manager")
        managers = manager_group.user_set.all()
        managers_names = [user.username for user in managers]
        data = {
            "Managers": managers_names,
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsManager):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, id=user_id)
        manager_group = Group.objects.get(name="manager")
        manager_group.user_set.add(user)
        data = {
            "Message": "User added to the manager group",
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


# /api/groups/manager/users/{userId}
class SingleManagerUserView(APIView):
    permission_classes = [IsManager]

    def delete(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsManager):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        user_id = kwargs.get("userId")
        user = get_object_or_404(User, id=user_id)
        manager_group = Group.objects.get(name="manager")

        if user in manager_group.user_set.all():
            manager_group.user_set.remove(user)
            data = {
                "Message": "User removed from the manager group",
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = {
                "Message": "User is not a manager",
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


# /api/groups/delivery-crew/users
class DeliveryCrewUsersView(APIView):
    permission_classes = [IsManager]

    def get(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsManager):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        delivery_crew_group = Group.objects.get(name="delivery_crew")
        delivery_crews = delivery_crew_group.user_set.all()
        delivery_crews_names = [user.username for user in delivery_crews]
        data = {
            "delivery_crews": delivery_crews_names,
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsManager):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, id=user_id)
        delivery_crew_group = Group.objects.get(name="delivery_crew")
        delivery_crew_group.user_set.add(user)
        data = {
            "Message": "User added to the delivery_crew group",
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


# /api/groups/delivery-crew/users/{userId}
class SingleDeliveryCrewUserView(APIView):
    permission_classes = [IsManager]

    def delete(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsManager):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        user_id = kwargs.get("userId")
        user = get_object_or_404(User, id=user_id)
        delivery_crew_group = Group.objects.get(name="delivery_crew")

        if user in delivery_crew_group.user_set.all():
            delivery_crew_group.user_set.remove(user)
            data = {
                "Message": "User removed from the delivery_crew group",
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = {
                "Message": "User is not a delivery_crew",
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


# Cart and Order management : /api/cart/menu-items
class CartMenuItemsView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request, *args, **kwargs):
        if not isinstance(request.user, IsCustomer):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        cart_tiem = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_tiem, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsCustomer):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        menu_item_id = request.data.get("menu_item_id")
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)

        existing_itme = Cart.objects.filter(user=request.user, menuitem=menu_item)

        if existing_itme:
            existing_itme.quantity += 1
            existing_itme.save()
        else:
            Cart.objects.create(user=request.user, menuitem=menu_item, quantity=1)

        data = {
            "Message": "Menu Item added to the cart",
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

    def delete(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsCustomer):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        menu_item_id = request.data.get("menu_item_id")
        Cart.objects.filter(user=request.user, menuitem_id=menu_item_id).delete()
        data = {
            "messsage": "Menu Item removed from the cart",
        }
        return Response(data=data, status=status.HTTP_200_OK)


# /api/orders
class OrdersView(APIView):
    permission_classes = [IsCustomer | IsManager | IsDeliveryCrew]

    def get(self, request: Request, *args, **kwargs):
        if isinstance(request.user, IsCustomer):
            orders = Order.objects.filter(user=request.user)
        elif isinstance(request.user, IsManager):
            orders = Order.objects.all()
        elif isinstance(request.user, IsDeliveryCrew):
            orders = Order.objects.filter(delivery_crew=request.user)
        else:
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsCustomer):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        cart_item = Cart.objects.filter(user=request.user)
        new_order = Order.objects.create(
            user=request.user, delivery_crew=request.delivery_crew
        )

        for item in cart_item:
            OrderItem.objects.create(
                order=new_order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.unit_price * item.quantity,
            )
        cart_item.delete()

        data = {
            "Message": "Order created",
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


# /api/orders/{orderId}
class SingleOrderView(APIView):
    permission_classes = [IsCustomer | IsManager | IsDeliveryCrew]

    def get(self, request: Request, *args, **kwargs):
        order_id = kwargs.get("orderId")
        order = get_object_or_404(Order, id=order_id)

        if request.user != order.user and not isinstance(request.user, IsManager):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(order.orderitem_set.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsDeliveryCrew):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        try:
            order_id = kwargs.get("orderId")
            order = get_object_or_404(Order, id=order_id)

            if not order.status:
                order.status = True
                order.save()
                data = {
                    "Message": "Order status updated",
                }
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                data = {
                    "Message": "Delivery is on the way",
                }
                return Response(data=data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            data = {
                "Message": "Order does not exist",
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, *args, **kwargs):
        if not isinstance(request.user, IsManager):
            data = {
                "Message": "Unauthorized access",
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        try:
            order_id = kwargs.get("orderId")
            order = get_object_or_404(Order, id=order_id)
            order.delete()
            data = {
                "Message": "Order deleted",
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            data = {
                "Message": "Order does not exist",
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
