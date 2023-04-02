from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class MyAccountManger(BaseUserManager):
    def create_user(self, first_name,last_name,username,email,phone_number,password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an username')
        

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self,first_name,last_name,email,username,password,phone_number):
        user=self.create_user(

            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number 

        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
     



class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=50)
    pic=models.ImageField(upload_to="pro_pic/",null=True,blank=True,default="static/img/userprofile.jpg" )



    #required


    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)


    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name','phone_number']


    objects=MyAccountManger()


    def __str__(self):
        return self.email
    
    def has_perm(self,pars,obj=None):
        return self.is_admin
    def has_module_perms(self,add_label):
        return True
    







# Create your models here.





class Address(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email_2=models.EmailField(max_length=100)
    house_name=models.CharField(max_length=250,unique=False)
    landmark=models.CharField(max_length=100)
    pincode=models.IntegerField()
    city=models.CharField(max_length=200,unique=False)
    district=models.CharField(max_length=100,unique=False)
    state=models.CharField(max_length=200,unique=False)
    country=models.CharField(max_length=150,unique=False)
    phone_number=models.CharField(max_length=100)
    default=models.BooleanField(default=False)


class UserOTP(models.Model):
    time_st=models.DateTimeField(auto_created=True,null=True)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    otp=models.IntegerField()
    