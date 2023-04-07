from django.shortcuts import render, redirect
from .forms import PollForm, Poll_Questions_Form, Poll_Questions_Options_Form
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from .models import Poll, Poll_Questions, Poll_Question_Options

# Create your views here.

def index(request):
    return render(request, 'website/index.html')
  
class CreatePollView(CreateView):
    template_name = 'website/crud/poll.html'
    success_url = reverse_lazy('create_question')
    model = Poll
    form_class = PollForm

    def form_valid(self, form):
        return super(CreatePollView, self).form_valid(form)
      
class CreateQuestionView(CreateView):
    template_name = 'website/crud/question.html'
    success_url = reverse_lazy('index')
    model = Poll_Questions
    form_class = Poll_Questions_Form

    def form_valid(self, form):
        return super(CreateQuestionView, self).form_valid(form)