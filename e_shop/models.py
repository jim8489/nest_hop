from itertools import product
from django.db import models
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

STATUS_CHOICE = {
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
}

STATUS = {
    ("draft", "Processing"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
}

RATING = {
    (1, "⭐☆☆☆☆"),
    (2, "⭐⭐☆☆☆"),
    (3, "⭐⭐⭐☆☆"),
    (4, "⭐⭐⭐⭐☆"),
    (5, "⭐⭐⭐⭐⭐"),
}

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    title= models.CharField(max_length=100, default="food")
    image = models.ImageField(upload_to="category", default="category.jpg")
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="ven", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="amazon")
    image = models.ImageField(upload_to="user_directory_path", default="vendor.jpg")
    cover_image = models.ImageField(upload_to="user_directory_path", default="vendor.jpg")

    #description = models.TextField(null=True, blank=True, default="i am a vendor")
    description = RichTextUploadingField(null=True, blank=True, default="I am a vendor")

    address = models.CharField(max_length=100, default="bangladesh")
    contact = models.CharField(max_length=100, default="01315199939")
    chat_resp_time = models.CharField(max_length=100, default=100)
    shipping_on_time = models.CharField(max_length=100, default=100)
    chat_resp_time = models.CharField(max_length=100, default=100)
    authentic_rating = models.CharField(max_length=100, default=100)
    days_return = models.CharField(max_length=100, default=100)
    warranty_period = models.CharField(max_length=100, default=100)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Vendors"
        
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
#class Tags(models.Model):
   # pass
    
class product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet="abcdefgh12345")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="products")

    
    title = models.CharField(max_length=100, default="fresh fruit")
    image = models.ImageField(upload_to="user_directory_path", default="product.jpg")
    
    #description = models.TextField(null=True, blank=True, default="This is the product")
    description = RichTextUploadingField(null=True, blank=True, default="This is the product")
    
    price= models.DecimalField(max_digits=65, decimal_places=2, default="1.99")
    old_price= models.DecimalField(max_digits=65, decimal_places=2, default="2.99")
    
    specifications= RichTextUploadingField(null=True, blank=True)
    #specifications= models.TextField(null=True, blank=True)

    type=models.CharField(max_length=100, default="Organic",  null=True, blank=True)
    stock_count=models.CharField(max_length=100, default="10", null=True, blank=True)
    life=models.CharField(max_length=100, default="100 Days", null=True, blank=True)
    mfd=models.DateTimeField(auto_now_add=False, null=True, blank=True)

    
    tags = TaggableManager(blank=True)
    
    #tags= models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    
    status= models.BooleanField(default=True)
    in_stock= models.BooleanField(default=True)
    featured= models.BooleanField(default=False)
    digital= models.BooleanField(default=False)
   
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")

    date = models.DateField(auto_now_add=True)
    updated = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Products"
        
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price= ((self.price - self.old_price)/self.old_price) * 100
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product.images", default="product.jpg")
    Product= models.ForeignKey(product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Images"
        
        
        
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price= models.DecimalField(max_digits=65, decimal_places=2, default="1.99")
    paid_status= models.BooleanField(default=False)
    order_date = models.DateField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS, max_length=30, default="processing")

    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order= models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no= models.CharField(max_length=200)
    product_status= models.CharField(max_length=200)
    item= models.CharField(max_length=200)
    image= models.CharField(max_length=200)
    qty= models.IntegerField(default=0)
    price= models.DecimalField(max_digits=65, decimal_places=2, default="1.99")
    total= models.DecimalField(max_digits=65, decimal_places=2, default="1.99")
    
    class Meta:
        verbose_name_plural = "Cart Order Items"
    
    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))
    
    

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Product = models.ForeignKey(product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None) 
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Review"
    
    def __str__(self):
        return self.Product.title  
    
    def get_rating(self):
        return self.rating
   

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Product = models.ForeignKey(product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"
        
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Address"