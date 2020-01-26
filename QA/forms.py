from django import forms
from .models import Question, Answer
from django.utils.translation import ugettext_lazy as _


class QuestionForm(forms.ModelForm):
    title = forms.CharField(max_length=100, label=_('Title'), required=True, help_text=_('Input your question here'),
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

    description = forms.CharField(max_length=1000, label=_('Description'), required=True,
                                  help_text=_('Input description of question here'),
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Question
        fields = ['title', 'description']


class AnswerForm(forms.ModelForm):
    description = forms.CharField(max_length=2000, label=_('Answer'), required=True,
                                  help_text=_('Write your answer here'),
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Answer
        fields = ['description']
