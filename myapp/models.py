from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Subject(models.Model):
    Subjectcode = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    credits = models.IntegerField()


class Teacher(models.Model):
    TeacherID = models.IntegerField(primary_key=True)
    subjectcode = models.ForeignKey(Subject, on_delete=models.CASCADE)
    Qualification = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)


# Menu model
class Menu(models.Model):
    item_name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)


class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)

    def __str__(self):
        return self.first_name
