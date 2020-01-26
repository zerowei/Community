from django.shortcuts import redirect
from .models import Profile
from authentication.models import MyUser
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.


@method_decorator([login_required], name='dispatch')
class ShowProfile(ListView):
    model = Profile
    template_name = "profile/ShowProfile.html"

    def get_context_data(self, **kwargs):
        context = super(ShowProfile, self).get_context_data(**kwargs)
        user_id = self.kwargs.get('pk')
        context['user'] = MyUser.objects.get(id=user_id)
        context['profile'] = Profile.objects.get(user=MyUser.objects.get(id=user_id))
        diff = MyUser.objects.get(id=user_id).totalexp - MyUser.objects.get(id=user_id).experience
        context['diff'] = diff
        return context


@method_decorator([login_required], name='dispatch')
class UpdateProfile(UpdateView):
    model = Profile
    fields = ['area', 'nickname', 'photo', 'job']
    template_name = "profile/UpdateProfile.html"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=MyUser.objects.get(id=self.kwargs.get('pk')))

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        form.save_m2m()
        return redirect('profile:ShowProfile', self.kwargs.get('pk'))

    def get_success_url(self):
        return redirect('profile:ShowProfile', self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(UpdateProfile, self).get_context_data(**kwargs)
        user_id = self.kwargs.get('pk')
        context['user'] = MyUser.objects.get(id=user_id)
        context['profile'] = Profile.objects.get(user=MyUser.objects.get(id=user_id))
        return context
