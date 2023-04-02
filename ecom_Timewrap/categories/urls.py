
from django.urls import path
from .import views



urlpatterns = [
path('category',views.category,name="category"),
path('category_edit/<int:id>',views.category_edit,name="category_edit"),
path('category_add/',views.category_add,name="category_add"),
path('category_delete/<int:id>',views.category_delete,name="category_delete"),
]