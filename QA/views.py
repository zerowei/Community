from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from myprofile.models import Profile
from authentication.models import MyUser
from .forms import QuestionForm, AnswerForm
# Create your views here.


@method_decorator([login_required], name='dispatch')
class CreateQuestionView(CreateView):
    model = Question
    template_name = "qa/CreateQuestion.html"
    form_class = QuestionForm

    def form_valid(self, form):
        question = form.save(commit=False)
        question.user = self.request.user
        question.update_date = question.create_date
        question.save()
        form.save_m2m()
        MyUser.objects.filter(id=self.request.user.id).update(experience=self.request.user.experience+8)
        experience = MyUser.objects.get(pk=self.request.user.id).experience
        level = MyUser.objects.get(pk=self.request.user.id).level
        totalexp = MyUser.objects.get(pk=self.request.user.id).totalexp
        if experience >= totalexp:
            MyUser.objects.filter(pk=self.request.user.id).update(level=level + 1)
            totalexp += (level + 1) * 100
        MyUser.objects.filter(pk=self.request.user.id).update(totalexp=totalexp)
        return redirect('qa:QuestionDetail', self.request.user.id, question.pk)


@method_decorator([login_required], name='dispatch')
class QuestionDetailView(CreateView):
    model = Answer
    template_name = "qa/QuestionDetail.html"
    form_class = AnswerForm

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        question_pk = self.kwargs['pk']
        user_id = self.kwargs['uid']
        question = Question.objects.get(pk=question_pk)
        profile = Profile.objects.get(user=question.user)
        user_profile = Profile.objects.get(user_id=user_id)
        context['question'] = question
        context['profile'] = profile
        context['userProfile'] = user_profile
        if Answer.objects.filter(question=question):
            answer = Answer.objects.filter(question=question)
            context['answers'] = answer
        return context


@login_required
def create_answer(request, pk):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.profile = Profile.objects.get(user_id=request.user.id)
            answer.question = Question.objects.get(pk=pk)
            answer.description = form.cleaned_data.get('description')
            answer.save()
            form.save_m2m()
            MyUser.objects.filter(id=request.user.id).update(experience=request.user.experience+5)
            experience = MyUser.objects.get(pk=request.user.id).experience
            level = MyUser.objects.get(pk=request.user.id).level
            totalexp = MyUser.objects.get(pk=request.user.id).totalexp
            if experience >= totalexp:
                MyUser.objects.filter(pk=request.user.id).update(level=level + 1)
                totalexp += (level + 1) * 100
            MyUser.objects.filter(pk=request.user.id).update(totalexp=totalexp)
            Question.objects.filter(pk=pk).update(update_date=answer.create_date)
            return redirect('qa:QuestionDetail', request.user.id, pk)
    else:
        form = AnswerForm()
    return redirect('qa:QuestionDetail', request.user.id, pk)


@method_decorator([login_required], name='dispatch')
class QuestionListView(ListView):
    model = Question
    template_name = "qa/QuestionList.html"
    context_object_name = 'questions'
    queryset = Question.objects.all()
    ordering = ['-update_date']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        user_id = self.kwargs['uid']
        profile = Profile.objects.get(user_id=user_id)
        context['profile'] = profile
        rate = MyUser.objects.get(id=user_id).experience / MyUser.objects.get(id=user_id).totalexp * 150
        context['rate'] = rate
        return context


@method_decorator([login_required], name='dispatch')
class MyQuestionsView(ListView):
    model = Question
    template_name = "qa/MyQuestions.html"
    context_object_name = 'questions'
    ordering = ['-update_date']
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(MyQuestionsView, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        profile = Profile.objects.get(user_id=user_id)
        context['profile'] = profile
        rate = MyUser.objects.get(id=user_id).experience / MyUser.objects.get(id=user_id).totalexp * 150
        context['rate'] = rate
        return context


@method_decorator([login_required], name='dispatch')
class MyAnswersView(ListView):
    model = Answer
    template_name = "qa/MyAnswers.html"
    context_object_name = 'answers'
    ordering = ['-update_date']
    paginate_by = 10

    def get_queryset(self):
        return Answer.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(MyAnswersView, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        profile = Profile.objects.get(user_id=user_id)
        context['profile'] = profile
        rate = MyUser.objects.get(id=user_id).experience / MyUser.objects.get(id=user_id).totalexp * 150
        context['rate'] = rate
        return context


@method_decorator([login_required], name='dispatch')
class ReplyMeView(ListView):
    model = Answer
    template_name = "qa/ReplyMe.html"
    context_object_name = 'answers'
    ordering = ['-update_date']
    paginate_by = 10

    def get_queryset(self):
        questions = Question.objects.filter(user=self.request.user)
        answers = Answer.objects.none()
        for question in questions:
            count = question.get_answer_count() - question.answer_count
            answer_keys = [key.pk for key in Answer.objects.filter(question=question).order_by("-id")[:count]]
            answer = Answer.objects.filter(id__in=answer_keys)
            answers = answers | answer
            Question.objects.filter(pk=question.pk).update(answer_count=question.get_answer_count())
        return answers

    def get_context_data(self, **kwargs):
        context = super(ReplyMeView, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        profile = Profile.objects.get(user_id=user_id)
        context['profile'] = profile
        rate = MyUser.objects.get(id=user_id).experience / MyUser.objects.get(id=user_id).totalexp * 150
        context['rate'] = rate
        return context


@login_required
def delete_question(request, pk):
    Question.objects.get(pk=pk).delete()
    Answer.objects.filter(question_id=pk).delete()
    return redirect('qa:QuestionList', request.user.id)


@login_required
def delete_answer(request, qid, aid):
    Answer.objects.filter(pk=aid).delete()
    return redirect('qa:QuestionDetail', request.user.id, qid)
