from django.urls import path, include
from .views import CreateQuestionView, QuestionDetailView, QuestionListView, \
                   create_answer, delete_question, delete_answer, MyQuestionsView, MyAnswersView, ReplyMeView

app_name = 'qa'
urlpatterns = [
    path('qa/', include(([
        path('<int:uid>/', QuestionListView.as_view(), name='QuestionList'),
        path('CreateQuestion/', CreateQuestionView.as_view(), name='CreateQuestion'),
        path('<int:uid>/detail/<int:pk>', QuestionDetailView.as_view(), name='QuestionDetail'),
        path('<int:pk>/CreateAnswer', create_answer, name='CreateAnswer'),
        path('<int:pk>/deleteQuestion', delete_question, name='deleteQuestion'),
        path('<int:qid>/<int:aid>/deleteAnswer', delete_answer, name='deleteAnswer'),
        path('MyQuestions/', MyQuestionsView.as_view(), name='MyQuestions'),
        path('MyReplies/', MyAnswersView.as_view(), name='MyReplies'),
        path('ReplyMe/', ReplyMeView.as_view(), name='ReplyMe'),
    ])))
]
