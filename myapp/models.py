from django.db import models

# Create your models here.
class ProductModel(models.Model):
    image=models.ImageField(upload_to="product_image/")
    product_name=models.CharField(max_length=50)
    price=models.FloatField()
    details=models.TextField(max_length=500)

class Registration(models.Model):
    profile=models.ImageField(upload_to="profile_image/")
    full_name=models.CharField(max_length=50)
    email=models.EmailField()
    user_name=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    choose=[
        ("Male","Male"),
        ("Female","Female")
    ]
    gender=models.CharField(max_length=10)
    dob=models.DateField()
    address=models.TextField(max_length=500)
    phone_number=models.IntegerField()

#####this is for superadmin
    def __str__(self):
        return self.user_name

class Validation(models.Model):
    fullname=models.CharField(max_length=50)
    username=models.CharField(max_length=20)
    email=models.EmailField()
    password=models.CharField(max_length=20)