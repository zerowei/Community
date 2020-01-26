from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from .forms import UserCreationForm
from .models import MyUser
from django.utils.timezone import now
# Create your views here.


class UserCreationView(CreateView):
    model = MyUser
    template_name = 'authentication/UserCreation.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return render(self.request, 'home/home.html')


def signin(request, pk):
    level = MyUser.objects.get(pk=pk).level
    totalexp = MyUser.objects.get(pk=pk).totalexp
    MyUser.objects.filter(pk=pk).update(experience=request.user.experience+10)
    experience = MyUser.objects.get(pk=pk).experience
    if experience >= totalexp:
        MyUser.objects.filter(pk=pk).update(level=level+1)
        totalexp += (level+1)*100
    MyUser.objects.filter(pk=pk).update(isSignin=True)
    MyUser.objects.filter(pk=pk).update(signdate=now().date())
    MyUser.objects.filter(pk=pk).update(totalexp=totalexp)
    return redirect('http://127.0.0.1:8000/')


