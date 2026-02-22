from django.db import models
from django.utils.text import slugify
from django.conf import settings 
from django.db.models import Q  
class Item(models.Model):
    CATEGORY =(("Shoes","SHOES"),
                ("Hat","HAT"),
                ("Shirt","SHIRT"),
                ("Pants","PANTS"),
                ("Coat","COAT"),
                ("Belt","BELT"),
                ("Tie","TIE"),
                ("Jewelry","JEWELRY"),
                ("Socks","SOCKS"),
                ("Bag","BAG")
                )
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True,null=True)
    image=models.ImageField(upload_to='img',null=True,blank=True)


    description=models.TextField(blank=True,null=True)
    price= models.DecimalField(max_digits=10,decimal_places=2)
    category=models.CharField(max_length=50,choices=CATEGORY,blank=True,null=True)

    def __str__(self):
        return self.name 
    
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug= slugify(self.name)
            unique_slug=self.slug
            counter = 1
            if Item.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{self.slug}-{counter}'
                counter +=1
            self.slug = unique_slug
        super().save(*args,**kwargs)






class Cart(models.Model):
    session_id= models.CharField(max_length=60,null=True,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add = True,blank=True,null=True)
    modified_at = models.DateTimeField(auto_now = True,blank=True,null=True)
    
    

    def __str__(self):
        if self.user:
            return f" Cart of {self.user.username}"
        return f"Guest Cart ({self.session_id})"
    
    
    



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='things',on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity= models.IntegerField(default=1)

   

   
    def __str__(self):
        if self.cart.user:
            return f"{self.quantity} x {self.item.name} in cart {self.cart.user.username}"
        return f"{self.quantity} x {self.item.name} in Guest cart {self.cart.session_id}"
    



class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True)
    status= models.CharField(max_length=200,choices=STATUS_CHOICES,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return  f" Order {self.id} - {self.user.username}" 







class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    item= models.ForeignKey(Item,on_delete=models.CASCADE )
    quantity=models.PositiveIntegerField(default=1)
    price= models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return  f"{self.quantity} x {self.item.name} in order {self.order.user.username}"


class Transaction(models.Model):
    ref= models.CharField(max_length=255,unique=True,)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    order = models.ForeignKey(Order ,related_name='transactions', on_delete=models.CASCADE)   
    currency = models.CharField(max_length=10, default='USD')
    status= models.CharField(max_length=20,default='pending')
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.ref} - {self.status}"
    




