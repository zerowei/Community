from django.shortcuts import render
from django.utils.timezone import now, timedelta
from authentication.views import MyUser
# Create your views here.


def home(request):
    if request.user.id:
        date = MyUser.objects.get(pk=request.user.id).signdate
        if now().date() >= (date + timedelta(days=1)):
            MyUser.objects.filter(pk=request.user.id).update(isSignin=False)
    return render(request, 'home/home.html')
