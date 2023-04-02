from django.urls import path
from .import views
from .import views2



urlpatterns = [
    
  
    

 
#................................................. user side urls.................................................................
    path('',views.store,name='store'),

    path('wishlist/',views.wishlist,name="wishlist"),
    path('wishlist/add_wishlist/<int:product_id>/', views.add_wishlist, name='add_wishlist'),    
    path('wishlist/remove_wishlistitem/<int:product_id>/', views.remove_wishlistitem, name='remove_wishlistitem'),    
         

    # carts urls
    path('cart/',views.cart_summary,name="cart"),
    path('add_cart/<int:product_id>/',views.add_cart,name="add_cart"),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart,name="remove_cart"),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',views.remove_cart_item,name="remove_cart_item"),

    path('category/<slug:category_slug>/',views.store,name="product_by_category"),
    path('brand/<slug:brand_slug>/',views.store,name="product_by_brand"),
    path('material/<slug:material_slug>/',views.store,name="product_by_material"),
    path('color/<slug:color_slug>/',views.store,name="product_by_color"),
    path('product_info/<slug:product_slug>/',views.product_info,name="product-info"),

    path('search/',views.search,name="search"),
    path('banner_view/',views.banner_view,name="banner_view"),

    path('checkout',views.checkout,name="checkout"),

    path('apply-coupon/', views.cart_summary, name="apply_coupon"),
    path('remove-coupon/', views.remove_coupon, name="remove_coupon"),

    path('default-address/<int:id>', views.default_address, name="default_address"),
   path('products/', views.store,name="price_sorting"),
    path('sort/', views.store,name="sorting"),

  





]