from django.urls import path
from .import views,views2





urlpatterns = [
    
#................................................. user side urls........................................................
path('sign_up/',views.sign_up,name="sign_up"),
path('login/',views.login,name="login"),
path('logout/',views.logout,name="logout"),

path('activate/<uidb64>/<token>/',views.activate,name="activate"),

path('otp_login/',views.otp_login,name="otp"),
path('otp_email/',views.otp_email,name="email"),

path('reset-password/',views.reset_password,name="reset_password"),
path('confirm-password/',views.confirm_password,name="confirm_password"),
path('reset-validation/<uidb64>/<token>/',views.reset_validation,name="reset_validation"),


path('profile/',views.profile,name="profile"),
path('edit_profile/<int:id>',views.edit_profile,name="edit_profile"),
path('address_view/',views.address_view,name="address_view"),
path('add_address/',views.add_address,name="add_address"),
path('address_delete/<int:id>/',views.address_delete,name="address_delete"),
path('edit_address/<int:id>/',views.edit_address,name="edit_address"),
path('dp_edit/',views.dp_edit,name="dp_edit"),

#................................................. admin side urls..........................................................

path('adm/user-list',views2.user_list,name="user_list"),
path('block_unblock/<int:id>/',views2.block_unblock,name="block_unblock")


]