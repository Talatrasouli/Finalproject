from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.

class Category(models.Model):
    title=models.CharField(max_length=200,verbose_name='category')
    slug=models.CharField(max_length=200,unique=True) 
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='subcategories')
    class Meta:
        ordering=['title']

    def __str__(self):
        return self.title
    


class City(models.Model):
    name=models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.name
    

# class User(models.Model):
#     email=models.EmailField()
#     first_name=models.CharField(max_length=100)
#     last_name=models.CharField(max_length=100)
#     user_name=models.CharField(max_length=200)
#     phone_number=models.CharField(max_length=12)
  
#     def __str__(self):
#         return self.user_name
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Ad.Status.ACTIVE)
       

    
class Ad(models.Model):
    class Status(models.TextChoices):
      
        ACTIVE=('AC', 'Active')
        INACTIVE=('IAC', 'Inactive')
        PENDING=('PD','Pending')

        
    # CATEGORY_CHOICES = (
    #     ('electronics', 'electronics'),
    #     ('fashion', 'fashion'),
    #     ('real_estate', 'real_estate'),
    #     ('cars', 'cars'),
    # )

    owner=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='advertisements_created_by',on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='advertisement_category')
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200,unique=True)
    overview=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created_at=models.DateTimeField(auto_now_add=True,)
    updated=models.DateTimeField(auto_now=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=20,decimal_places=3,null=True,blank=True)
    phone_number=models.CharField(max_length=12)
    image=models.ImageField(upload_to='advertisement_images',null=True,blank=True)
    city= city=models.ForeignKey(City,on_delete=models.CASCADE,blank=True,null=True,related_name='advertisement_city')
    active=models.DateTimeField(default=timezone.now)
    status=models.CharField(max_length=3,choices=Status.choices,default=Status.INACTIVE)
   
    # user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='advertisement_user')
    

    objects=models.Manager()
    active=ActiveManager()

    class Meta:
        ordering=['-created_at']
        indexes=[
            models.Index(fields=['-created_at'])
        ]
        def __str__(self):
            return self.title
        
class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ad_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.ad.title}"