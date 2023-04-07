from django.urls import path
from website import views

urlpatterns = [
  path('', views.index, name='index'),
  path('create_poll/', views.CreatePollView.as_view(), name='create_poll'),
  path('create_question/', views.CreateQuestionView.as_view(), name='create_question')
  
]
