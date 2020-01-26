from django.db import models
from authentication.views import MyUser
from django.db.models.signals import post_save
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    area = models.CharField(max_length=50, null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    photo = models.ImageField(upload_to='user_images', max_length=100, default='image/user.png')
    photo_90x90 = ImageSpecField(source="photo", processors=[ResizeToFill(90, 90)],
                                 format='JPEG', options={'quality': 95})
    job = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Profile'

    def __unicode__(self):
        return self.nickname


def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


def save_profile(sender, instance, **kwargs):
        instance.profile.save()


post_save.connect(create_profile, sender=MyUser)
post_save.connect(save_profile, sender=MyUser)
