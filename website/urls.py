from django.urls import path
from website.views import *

urlpatterns = [
    path('', index, name='index'),
    path('polls/', PollListView.as_view(), name='polls'),
    path('create_poll/', CreatePollView.as_view(), name='create_poll'),
    path('update_poll/<int:pk>', UpdatePollView.as_view(), name='update_poll'),
    path('delete_poll/<int:pk>', DeletePollView.as_view(), name='delete_poll'),    
    path('questions/<int:poll_pk>', QuestionListView.as_view(),name='questions'),
    path('create_question/<int:poll_pk>', CreateQuestionView.as_view(),name='create_question'),
    path('update_question/<int:poll_pk>/<int:pk>', UpdateQuestionView.as_view(),name='update_question'),
    path('delete_question/<int:poll_pk>/<int:pk>', DeleteQuestionView.as_view(),name='delete_question'),
    path('options/<int:question_pk>', OptionListView.as_view(),name='options'),
    path('create_option/<int:question_pk>', CreateOptionView.as_view(),name='create_option'),
    path('update_option/<int:question_pk>/<int:pk>', UpdateOptionView.as_view(),name='update_option'),
    path('delete_option/<int:question_pk>/<int:pk>', DeleteOptionView.as_view(),name='delete_option'),
]
