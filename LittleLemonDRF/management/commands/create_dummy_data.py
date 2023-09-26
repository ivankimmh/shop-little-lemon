from django.core.management import BaseCommand
from django.contrib.auth.models import User, Group
from LittleLemonDRF.models import Category, MenuItem, Cart, Order, OrderItem


import random
from faker import Faker

import datetime


class Command(BaseCommand):
    help = "Create random dummy data without using django_seed"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Groups
        for name in ["manager", "customer", "delivery_crew"]:
            Group.objects.get_or_create(name=name)

        # Create Users with Groups
        for _ in range(10):
            user = User.objects.create(
                username=fake.user_name(), email=fake.email(), password="1234"
            )
            group_name = random.choice(["manager", "customer", "delivery_crew"])
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

        # Create Categories
        for name in ["Pizza", "Burger", "Pasta"]:
            Category.objects.create(slug=fake.slug(), title=name)

        # Create MenuItems
        for _ in range(10):
            MenuItem.objects.create(
                title=fake.word(),
                price=round(random.uniform(10, 50), 2),
                featured=fake.boolean(),
                category=random.choice(Category.objects.all()),
            )

        # Create Cart
        for _ in range(5):
            Cart.objects.create(
                user=random.choice(User.objects.all()),
                menuitem=random.choice(MenuItem.objects.all()),
                quantity=random.randint(1, 5),
                unit_price=round(random.uniform(10, 50), 2),
                price=round(random.uniform(10, 50), 2),
            )

        # Create Order
        for _ in range(5):
            Order.objects.create(
                user=random.choice(User.objects.all()),
                unit_price=round(random.uniform(100, 500), 2),
                data=datetime.date.today(),
            )

        # Create OrderItem
        for _ in range(10):
            OrderItem.objects.create(
                order=random.choice(Order.objects.all()),
                menuitem=random.choice(MenuItem.objects.all()),
                quantity=random.randint(1, 5),
                unit_price=round(random.uniform(10, 50), 2),
                price=round(random.uniform(10, 50), 2),
            )

        self.stdout.write(self.style.SUCCESS("Dummy data created"))
