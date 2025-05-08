# This is  a model for a elaerning paltform
from django.db import models
from users.models import UserAccount
from django.utils.text import slugify

#course
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table="category"
        verbose_name_plural="Categories"
        # order by number of courses in each category
        ordering=["-created_at"]    
    
    
class Course(models.Model):
    title=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    price=models.DecimalField(max_digits=8,decimal_places=2,default=0.0)
    instructor=models.ForeignKey(
        UserAccount,on_delete=models.CASCADE,limit_choices_to={'role': 'instructor'}, related_name='courses')
    category=models.ForeignKey(
        Category,on_delete=models.CASCADE,related_name="courses")
    thumbnail=models.ImageField(upload_to="course_thumbnails/%Y/%m/%d/",blank=True,null=True)
    is_published=models.BooleanField(default=False)
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


    class Meta:
        db_table="course"
        verbose_name_plural="Courses"
        ordering=["-created_at"]
        
    
#Section Model
class Section(models.Model):
    title=models.CharField(max_length=150)
    course=models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='enrollments'
    )
    order=models.PositiveIntegerField()
    is_free=models.BooleanField(default=False)
    video=models.FileField(upload_to="videos/",null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} :: {self.course.title}"
    
    def can_change(self,user):
        return self.course.can_change(UserAccount)
    
    
    class Meta:
        db_table = "section"
        verbose_name_plural = "Sections"
        ordering = ["order"]
        unique_together = ["course", "title"]
        
    
# cart model
    class Cart(models.Model):
        UserAccount=models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name="cart")
    
#Enrollment model
class Enrollment(models.Model):
    student=models.ForeignKey(
        UserAccount,on_delete=models.CASCADE,limit_choices_to={'role': 'student'}, related_name='enrollments'
    )
    
    course=models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='enrollments'
        
    )
    completed=models.BooleanField(default=False)
    certificate_issued=models.BooleanField(default=False)
    last_accessed = models.DateTimeField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
     # This method defines how each enrollment will be shown as a string (e.g., in admin panel or logs)
    def __str__(self):
       return f"{self.student.full_name} -> {self.course.title}"
    class Meta:
        db_table="enrollment"
        verbose_name_plural="Enrollments"
        ordering=["-created_at"]
        unique_together = ["student", "course"]
        

    
#Payment model
#review model ,discussion model , progress model, reply of the comment model will be fo fututre features,   
