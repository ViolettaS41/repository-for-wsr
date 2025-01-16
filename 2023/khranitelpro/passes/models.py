from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True,null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
    )

class Department(models.Model):
    name = models.CharField(max_length=100)

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

class PassRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= True, blank=True)
    visit_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    visitor_first_name = models.CharField(max_length=50)
    visitor_last_name = models.CharField(max_length=50)
    visitor_middle_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    passport_series = models.CharField(max_length=4)
    passport_number = models.CharField(max_length=6)
    note = models.TextField()
    status = models.CharField(max_length=20, choices= [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending')

