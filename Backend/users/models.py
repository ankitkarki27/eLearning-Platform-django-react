from django.db import models
from django.contrib.auth.models import (
     AbstractBaseUser,
     BaseUserManager,PermissionsMixin
     )
# Create your models here.
class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("User must have email")
        
        user=self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password,**kwargs):
        user=self.create_user(
            email,
            password=password,**kwargs,
        )
        user.is_staff=True
        user.is_superuser=True
        user.role="admin"
        user.save(using=self.db)
        return user
    
    # UserAccount Model
class UserAccount(AbstractBaseUser,PermissionsMixin):
        #role choices for user type
        ROLE_CHOICES=[
            ("admin","Admin"),
            ("student","Student"),
            ("instructor","Instructor"),
        ]
        email=models.EmailField(
            verbose_name="email address",max_length=225,unique=True,
            
        )
        
        full_name=models.CharField(max_length=225)
        phone_number = models.CharField(max_length=10, blank=True, null=True)
        role=models.CharField(max_length=10,choices=ROLE_CHOICES,default="student",)
        profile_image=models.ImageField(
            upload_to="profile_images/%Y/%m/%d/",
            blank=True,
            null=True,
            default="profile_images/user_default.jpg",
            )
        
        is_verified=models.BooleanField(default=False)
        is_active=models.BooleanField(default=True)
        is_staff=models.BooleanField(default=False)
        is_superuser = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        
        objects = UserAccountManager()

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['full_name']

        #returns the string representation of the user object
        def __str__(self):
            return f"{self.full_name} ({self.email}) - {self.role}"

        class Meta:
            db_table = "lms_users"
            verbose_name_plural = "lms_users"
            ordering = ["-created_at"]
            