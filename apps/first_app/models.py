from django.db import models
import re
import bcrypt
emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')


class UserManager(models.Manager):
    def registration_validator(self,postData):
        errors ={}
        if len(postData['first_name'])<2:
            errors['first_name'] = "First name needs to be more than 2 characters"
        
        if len(postData["last_name"])<2:
            errors["last_name"] = "Lastname needs to be more than 2 characters"

        if len(postData["email"])<0:
            errors["email"] = "Email can't be blank"
        if not emailRegex.match(postData["email"]):
            errors["email"] = "Email already taken"

        if len(postData["password"])<0:
            errors["password"] = "Password can't be blank"
        if not passwordRegex.match(postData["password"]):
            errors ["password"] = "Password must contain at least one lowercase letter, one uppercase letter, and one digit"

        if postData["password"] != postData["confirm_password"]:
            errors["password"] = "Password must match"

        
        return errors
    
    def login_validator(self,postData):
        errors={}
        user=User.objects.filter(email=postData['email'])
        if not user:
            errors['email'] = 'Email is not registered or incorrect'
        if user and not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['password']='Password is incorrect'
        return errors
        

class WishManager(models.Manager):
    def wish_validator(self,postData):
        errors={}
        if len(postData['wish_title'])<3:
            errors['wish_title'] = "Needs to be more than 3 characters"
        
        if len(postData['wish_description'])<2:
            errors['wish_description'] = "Description needs to be more than 3 characters"
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    objects = UserManager()

class Wish(models.Model):
    title = models.CharField(max_length=255)
    description= models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User,related_name="wishes",)
    objects = WishManager()


# Create your models here.
