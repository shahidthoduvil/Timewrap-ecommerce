from django.urls import path
from .import views



urlpatterns = [
    
  


path('list-product',views.list_product,name="list_product"),
path('product_edit/<int:id>/',views.product_edit,name="product_edit"),
path('add-product',views.add_product,name="add_product"),
path('list-product/product_delete/<int:id>/',views.product_delete,name="product_delete"),


path('color',views.color,name="color"),
path('color/color_edit/<int:id>/',views.color_edit,name="color_edit"),
path('color/color_delete/<int:id>/',views.color_delete,name="color_delete"),
path('color/color_add/',views.color_add,name="color_add"),

path('material',views.material,name="material"),
path('material_edit/<int:id>/',views.material_edit,name="material_edit"),
path('material_delete/<int:id>/',views.material_delete,name="material_delete"),
path('material_add/',views.material_add,name="material_add"),

path('brand',views.brand,name="brand"),
path('brand_edit/<int:id>/',views.brand_edit,name="brand_edit"),
path('brand_delete/<int:id>/',views.brand_delete,name="brand_delete"),
path('brand_add/',views.brand_add,name="brand_add"),
    
path('banner',views.banner,name="banner"),
path('banner_delete/<int:id>',views.banner_delete,name="banner_delete"),
path('banner_add/',views.banner_add,name="banner_add"),
path('banner_edit/<int:id>',views.banner_edit,name="banner_edit"),

path('color-variant/',views.color_variant,name="color_variant"),
path('varaint_add/',views.varaint_add,name="variant_add"),
path('variant_edit/<int:id>',views.variant_edit,name="variant_edit"),
path('varaint_delete/<int:id>',views.varaint_delete,name="varaint_delete"),



]
    
