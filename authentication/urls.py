from django.urls import path
from authentication import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'authentication'
urlpatterns = [
    path('signup/', views.UserCreationView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('<int:pk>/signin', views.signin, name='signIn'),
]