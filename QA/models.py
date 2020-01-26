from django.db import models
from authentication.models import MyUser
from myprofile.models import Profile
# Create your models here.


class Question(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    answer_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ('-update_date',)

    def __unicode__(self):
        return self.title

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def get_answer_count(self):
        return Answer.objects.filter(question=self).count()


class Answer(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ('create_date',)

    def __unicode__(self):
        return self.description
