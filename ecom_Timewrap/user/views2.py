
from django.shortcuts import render,redirect,get_object_or_404
from .models import Account,Address


# .................................admin_side views.................................
def user_list(request):
    user_dict={
        'user_list':Account.objects.all().order_by('id')
    }
  

    return render(request,"admin_side/user_list.html",user_dict)





def block_unblock(request,id):

    user=get_object_or_404(Account,id=id)

    if user.is_active:

        user.is_active=False

        user.save()

        return redirect(user_list)
    
    else:

        user.is_active=True

        user.save()

        return redirect(user_list)

   
 

