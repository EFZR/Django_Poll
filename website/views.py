from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import PollForm, Poll_Questions_Form, Poll_Questions_Options_Form
from .models import Poll, Poll_Questions, Poll_Question_Options
from logging import log

# Create your views here.


def index(request):
    return render(request, 'website/index.html')


# class CreatePollView_ToQuestion(CreateView):
#     template_name = 'website/crud/poll.html'
#     model = Poll
#     form_class = PollForm
#     parameter = None

#     def form_valid(self, form):
#         return super(CreatePollView_ToQuestion, self).form_valid(form)

#     # get_success_url is a method that returns the URL to redirect to after processing a valid form.
#     def get_success_url(self):
#         return reverse_lazy('create_question', kwargs={'pk': self.object.id})


class PollListView(ListView):
    template_name = 'website/poll_list.html'
    model = Poll
    context_object_name = 'polls'


class CreatePollView(CreateView):
    template_name = 'website/poll_form.html'
    model = Poll
    form_class = PollForm
    parameter = None
    success_url = reverse_lazy('polls')

    def form_valid(self, form):
        messages.success(self.request, 'Poll created successfully')
        return super(CreatePollView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Poll creation failed')
        return super().form_invalid(form)


class UpdatePollView(UpdateView):
    template_name = 'website/poll_form.html'
    model = Poll
    form_class = PollForm
    success_url = reverse_lazy('polls')

    def form_valid(self, form):
        messages.success(self.request, 'Poll updated successfully')
        return super(UpdatePollView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Poll update failed')
        return super().form_invalid(form)


class DeletePollView(DeleteView):
    template_name = 'website/poll_delete.html'
    model = Poll
    success_url = reverse_lazy('polls')
    context_object_name = 'poll'

    def form_valid(self, form):
        messages.success(self.request, 'Poll deleted successfully')
        return super(DeletePollView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Poll deletion failed')
        return super().form_invalid(form)


class QuestionListView(ListView):
    model = Poll_Questions
    context_object_name = 'questions'
    template_name = 'website/question_list.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['poll'] = Poll.objects.get(id=self.kwargs['poll_pk'])
        return context

    def get_queryset(self):
        return Poll_Questions.objects.filter(poll_id=self.kwargs['poll_pk'])


class CreateQuestionView(CreateView):
    template_name = 'website/question_form.html'
    model = Poll_Questions
    form_class = Poll_Questions_Form

    def form_valid(self, form):
        messages.success(self.request, 'Question created successfully')
        form.instance.poll_id = self.kwargs['poll_pk']
        return super(CreateQuestionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Question creation failed')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateQuestionView, self).get_context_data(**kwargs)
        context['poll'] = Poll.objects.get(id=self.kwargs['poll_pk'])
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('questions', kwargs={'poll_pk': self.kwargs['poll_pk']})


class UpdateQuestionView(UpdateView):
    template_name = 'website/question_form.html'
    model = Poll_Questions
    form_class = Poll_Questions_Form

    def form_valid(self, form):
        messages.success(self.request, 'Question updated successfully')
        return super(UpdateQuestionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Question update failed')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateQuestionView, self).get_context_data(**kwargs)
        context['poll'] = Poll.objects.get(id=self.kwargs['poll_pk'])
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('questions', kwargs={'poll_pk': self.kwargs['poll_pk']})


class DeleteQuestionView(DeleteView):
    template_name = 'website/question_delete.html'
    model = Poll_Questions
    context_object_name = 'question'

    def form_valid(self, form):
        messages.success(self.request, 'Question deleted successfully')
        return super(DeleteQuestionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Question deletion failed')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(DeleteQuestionView, self).get_context_data(**kwargs)
        context['poll'] = Poll.objects.get(id=self.kwargs['poll_pk'])
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('questions', kwargs={'poll_pk': self.kwargs['poll_pk']})


class OptionListView(ListView):
    model = Poll_Question_Options
    context_object_name = 'options'
    template_name = 'website/option_list.html'

    def get_context_data(self, **kwargs):
        context = super(OptionListView, self).get_context_data(**kwargs)
        context['question'] = Poll_Questions.objects.get(
            id=self.kwargs['question_pk'])
        return context

    def get_queryset(self):
        return Poll_Question_Options.objects.filter(question_id=self.kwargs['question_pk'])


class CreateOptionView(CreateView):
    template_name = 'website/option_form.html'
    model = Poll_Question_Options
    form_class = Poll_Questions_Options_Form

    def form_valid(self, form):
        messages.success(self.request, 'Option created successfully')
        form.instance.question_id = self.kwargs['question_pk']
        return super(CreateOptionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Option creation failed')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateOptionView, self).get_context_data(**kwargs)
        context['question'] = Poll_Questions.objects.get(
            id=self.kwargs['question_pk'])
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('options', kwargs={'question_pk': self.kwargs['question_pk']})
      
      
class UpdateOptionView(UpdateView):
    template_name = 'website/option_form.html'
    model = Poll_Question_Options
    form_class = Poll_Questions_Options_Form

    def form_valid(self, form):
        messages.success(self.request, 'Option updated successfully')
        return super(UpdateOptionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Option update failed')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateOptionView, self).get_context_data(**kwargs)
        context['question'] = Poll_Questions.objects.get(
            id=self.kwargs['question_pk'])
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('options', kwargs={'question_pk': self.kwargs['question_pk']})
      
      
class DeleteOptionView(DeleteView):
    template_name = 'website/option_delete.html'
    model = Poll_Question_Options
    context_object_name = 'option'

    def form_valid(self, form):
        messages.success(self.request, 'Option deleted successfully')
        return super(DeleteOptionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Option deletion failed')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(DeleteOptionView, self).get_context_data(**kwargs)
        context['question'] = Poll_Questions.objects.get(
            id=self.kwargs['question_pk'])
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('options', kwargs={'question_pk': self.kwargs['question_pk']})
