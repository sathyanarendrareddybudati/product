from django.db import models

class Product(models.Model):
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    stock = models.PositiveIntegerField()
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    thumbnail = models.URLField()
    images = models.JSONField()  

class Comment(models.Model):

    body = models.TextField()
    post_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()
    username = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)

