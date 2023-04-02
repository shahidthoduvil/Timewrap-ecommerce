from django.db import models
from django.urls import reverse
from user.models import Account

# Create your models here.


class Category(models.Model):
    category_name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
     
    class Meta:
       verbose_name_plural='categories'

    def __str__(self):
        return  self.category_name
    

    def get_url(self):
       return reverse("product_by_category", args=[self.slug])
    



class Brand(models.Model):
    brand_name=models.CharField(max_length=250,default='un-branded')
    brand_image=models.ImageField(upload_to='brand_img/', blank=True)
    slug=models.SlugField(max_length=250,unique=True)

    class Meta:
        verbose_name_plural='brands'
    
    def __str__(self):
        return self.brand_name
    
    def get_url(self):
       return reverse("product_by_brand", args=[self.slug])
    
    

class Color(models.Model):
    color_name=models.CharField(max_length=250,blank=True)
    slug=models.SlugField(max_length=250,unique=True)
    class Meta:
        verbose_name_plural='colors'

    def __str__(self):
        return self.color_name
    
    def get_url(self):
       return reverse("product_by_color", args=[self.slug])

      


class Material(models.Model):
    material_name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    class Meta:
        verbose_name_plural='materials'

    def __str__(self):
        return self.material_name
    
    def get_url(self):
       return reverse("product_by_material", args=[self.slug])
    

class Product(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    specification=models.TextField(blank=True)
    slug = models.SlugField(max_length=250)
    price = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='images/', blank=True)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    sample = models.TextField(null=True,blank=True)


    class Meta:
        verbose_name_plural = 'products'

 
    def __str__(self):
         return str(self.title)
    
    def get_product_price(self):
        return self.price


    def get_url(self):
        return reverse('product-info', args=[self.slug ])
    
   
    #  + Variation.objects.get(product=self.id ,color=variant).price

    



class Variation(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    is_active=models.BooleanField(default=True)
    color=models.ForeignKey(Color,on_delete=models.SET_NULL,null=True)
    created_date=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.variation = f"{self.color}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.color.color_name
    
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20)
    discount_price = models.PositiveIntegerField(default=799)
    min_amount = models.PositiveIntegerField(default=17999)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.coupon_code
    





class Cart(models.Model):
    date_added=models.DateField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid=models.BooleanField(default=False)
    razor_pay_order_id=models.CharField(max_length=100,null=True,blank=True,unique=True)
    user=models.ForeignKey(Account, on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.user.email
    

    def get_cart_total(self):
        cart_items = CartItem.objects.filter(cart=self.id)
        price = []
        for cart_item in cart_items:
            quantity = cart_item.quantity
            price.append(cart_item.product.price * quantity)
            # if cart_item.variant:
            #     price.append(cart_item.variant.price * quantity)

        if self.coupon:
            if self.coupon.min_amount < sum(price):
                return sum(price) - self.coupon.discount_price
            
        return sum(price)

    # Tax of cart_total
    def get_tax(self):
        return round(0.025 * self.get_cart_total(), 2)

    # tax + cart_total
    def get_grand_total(self):
        return self.get_cart_total() + self.get_tax()
    
    
class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variation, on_delete=models.SET_NULL, null=True, blank=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
         
    def __str__(self):
      return str(self.product.id)
    
    
    def get_product_price(self):
        return self.product.price



    def get_sub_total(self):
        return self.product.price * self.quantity
   


 
    



class Banner(models.Model):
    heading=models.CharField(max_length=50,blank=True)
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='banner/',blank=True)

    def __str__(self):
        return self.heading
    

class Wishlist(models.Model):
    user=models.ForeignKey(Account, on_delete=models.SET_NULL,related_name="wishlist",null=True)
    
    def __str__(self):
        return str(self.user)
    
class WishlistItem(models.Model):
    wishlist=models.ForeignKey(Wishlist,on_delete=models.CASCADE,related_name="wishlist_item")
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(null=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):

        return self.product.title
    
class MultipleImg(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    img=models.ImageField(upload_to='MultipleImg/',blank=True)

    def __str__(self):
        return self.product.title
    

