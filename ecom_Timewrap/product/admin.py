from django.contrib import admin
from . models import *
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display= ('category_name','slug')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('brand_name',)}
    list_display= ('brand_name','brand_image','slug')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('color_name',)}
    list_display= ('color_name','slug')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('material_name',)}
    list_display= ('material_name','slug')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display= ('title','description','specification','brand','color','material','category','stock','image','is_available','created_date','modified_date','price','slug')

class CartAdmin(admin.ModelAdmin):
    list_display=('user','date_added','coupon','razor_pay_order_id')

admin.site.register(Cart,CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display=('product','cart','quantity','is_active','variant')
admin.site.register(CartItem,CartItemAdmin)

admin.site.register(Banner)

admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(MultipleImg)

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display=('product','color','is_active')
    list_editable=('is_active',)
    list_filter=('product','color','is_active')
    model=Variation

# admin.site.register(Variation,VariationAdmin)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_code', 'min_amount','discount_price', 'is_expired')

