from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Count, Prefetch
from django.contrib import messages
from django.contrib.auth import login
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PollForm, Poll_Questions_Form, Poll_Questions_Options_Form, LoginForm, SignUpForm
from .models import Poll, Poll_Questions, Poll_Question_Options, Poll_Question_Responses
from Logging.logger_base import log

# get_success_url is a method that returns the URL to redirect to after processing a valid form.


class Login(LoginView):
    template_name = 'website/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    form_class = LoginForm

    def get_success_url(self):
        messages.success(self.request, 'Login successful')
        log.info(f'User {self.request.user.username} registered successfully')
        return reverse_lazy('index')


class Register(FormView):
    template_name = 'website/register.html'
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            messages.success(self.request, 'Registration successful')
            log.info(f'User {user.username} registered successfully')
            login(self.request, user)

        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(Register, self).get(*args, **kwargs)


class IndexListView(LoginRequiredMixin, ListView):
    model = Poll
    context_object_name = 'polls'
    template_name = 'website/index.html'

    def get_queryset(self):
        return Poll.objects.filter(is_active=True)


class PollListView(LoginRequiredMixin, ListView):
    template_name = 'website/poll_list.html'
    model = Poll
    context_object_name = 'polls'


class CreatePollView(LoginRequiredMixin, CreateView):
    template_name = 'website/poll_form.html'
    model = Poll
    form_class = PollForm
    parameter = None
    success_url = reverse_lazy('polls')

    def form_valid(self, form):
        messages.success(self.request, 'Poll created successfully')
        log.info('Poll created successfully')
        return super(CreatePollView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Poll creation failed')
        log.error('Poll creation failed')
        return super().form_invalid(form)


class UpdatePollView(LoginRequiredMixin, UpdateView):
    template_name = 'website/poll_form.html'
    model = Poll
    form_class = PollForm
    success_url = reverse_lazy('polls')

    def form_valid(self, form):
        messages.success(self.request, 'Poll updated successfully')
        log.info('Poll updated successfully')
        return super(UpdatePollView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Poll update failed')
        log.error('Poll update failed')
        return super().form_invalid(form)


class DeletePollView(LoginRequiredMixin, DeleteView):
    template_name = 'website/poll_delete.html'
    model = Poll
    success_url = reverse_lazy('polls')
    context_object_name = 'poll'

    def form_valid(self, form):
        messages.success(self.request, 'Poll deleted successfully')
        log.info('Poll deleted successfully')
        return super(DeletePollView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Poll deletion failed')
        log.error('Poll deletion failed')
        return super().form_invalid(form)


class QuestionListView(LoginRequiredMixin, ListView):
    model = Poll_Questions
    context_object_name = 'questions'
    template_name = 'website/question_list.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['poll'] = Poll.objects.get(id=self.kwargs['poll_pk'])
        return context

    def get_queryset(self):
        return Poll_Questions.objects.filter(poll_id=self.kwargs['poll_pk'])


class CreateQuestionView(LoginRequiredMixin, CreateView):
    template_name = 'website/question_form.html'
    model = Poll_Questions
    form_class = Poll_Questions_Form

    def form_valid(self, form):
        form.instance.poll_id = self.kwargs['poll_pk']
        messages.success(self.request, 'Question created successfully')
        log.info('Question created successfully')
        return super(CreateQuestionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Question creation failed')
        log.error('Question creation failed')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateQuestionView, self).get_context_data(**kwargs)
        context['poll'] = Poll.objects.get(id=self.kwargs['poll_pk'])
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('questions', kwargs={'poll_pk': self.kwargs['poll_pk']})


class UpdateQuestionView(LoginRequiredMixin, UpdateView):
    template_name = 'website/question_form.html'
    model = Poll_Questions
    form_class = Poll_Questions_Form

    def form_valid(self, form):
        messages.success(self.request, 'Question updated successfully')
        log.info('Question updated successfully')
        return super(UpdateQuestionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Question update failed')
        log.error('Question update failed')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateQuestionView, self).get_context_data(**kwargs)
        context['poll'] = Poll.objects.get(id=self.kwargs['poll_pk'])
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('questions', kwargs={'poll_pk': self.kwargs['poll_pk']})


class DeleteQuestionView(LoginRequiredMixin, DeleteView):
    template_name = 'website/question_delete.html'
    model = Poll_Questions
    context_object_name = 'question'

    def form_valid(self, form):
        messages.success(self.request, 'Question deleted successfully')
        log.info('Question deleted successfully')
        return super(DeleteQuestionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Question deletion failed')
        log.error('Question deletion failed')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(DeleteQuestionView, self).get_context_data(**kwargs)
        context['poll'] = Poll.objects.get(id=self.kwargs['poll_pk'])
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('questions', kwargs={'poll_pk': self.kwargs['poll_pk']})


class OptionListView(LoginRequiredMixin, ListView):
    model = Poll_Question_Options
    context_object_name = 'options'
    template_name = 'website/option_list.html'

    def get_context_data(self, **kwargs):
        context = super(OptionListView, self).get_context_data(**kwargs)
        context['question'] = temp_id_question = Poll_Questions.objects.get(
            id=self.kwargs['question_pk'])
        context['poll'] = Poll.objects.get(id=temp_id_question.poll_id)
        return context

    def get_queryset(self):
        return Poll_Question_Options.objects.filter(question_id=self.kwargs['question_pk'])


class CreateOptionView(LoginRequiredMixin, CreateView):
    template_name = 'website/option_form.html'
    model = Poll_Question_Options
    form_class = Poll_Questions_Options_Form

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['question_pk']
        messages.success(self.request, 'Option created successfully')
        log.info('Option created successfully')
        return super(CreateOptionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Option creation failed')
        log.error('Option creation failed')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateOptionView, self).get_context_data(**kwargs)
        context['question'] = Poll_Questions.objects.get(
            id=self.kwargs['question_pk'])
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('options', kwargs={'question_pk': self.kwargs['question_pk']})


class UpdateOptionView(LoginRequiredMixin, UpdateView):
    template_name = 'website/option_form.html'
    model = Poll_Question_Options
    form_class = Poll_Questions_Options_Form

    def form_valid(self, form):
        messages.success(self.request, 'Option updated successfully')
        log.info('Option updated successfully')
        return super(UpdateOptionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Option update failed')
        log.error('Option update failed')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateOptionView, self).get_context_data(**kwargs)
        context['question'] = Poll_Questions.objects.get(
            id=self.kwargs['question_pk'])
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('options', kwargs={'question_pk': self.kwargs['question_pk']})


class DeleteOptionView(LoginRequiredMixin, DeleteView):
    template_name = 'website/option_delete.html'
    model = Poll_Question_Options
    context_object_name = 'option'

    def form_valid(self, form):
        messages.success(self.request, 'Option deleted successfully')
        log.info('Option deleted successfully')
        return super(DeleteOptionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Option deletion failed')
        log.error('Option deletion failed')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(DeleteOptionView, self).get_context_data(**kwargs)
        context['question'] = Poll_Questions.objects.get(
            id=self.kwargs['question_pk'])
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('options', kwargs={'question_pk': self.kwargs['question_pk']})


class VoteView(LoginRequiredMixin, TemplateView):
    template_name = 'website/vote.html'
    context_object_name = 'response'

    def get_context_data(self, **kwargs):
        context = super(VoteView, self).get_context_data(**kwargs)
        context['poll'] = poll = Poll.objects.get(id=self.kwargs['poll_pk'])
        context['questions'] = questions = Poll_Questions.objects.filter(
            poll_id=poll.id)
        self.rows = questions.count()
        options = []
        for question in questions:
            options.append(Poll_Question_Options.objects.filter(
                question_id=question.id))

        context['options'] = options
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        my_object = []
        questions = Poll_Questions.objects.filter(
            poll_id=self.kwargs['poll_pk'])
        # insert multiple lines in a table using django bulk_create() method
        if questions:
            for question in questions:
                poll_id = request.POST.get('poll_id', None)
                question_id = request.POST.get(
                    f'question_id{question.id}', None)
                option_id = request.POST.get(f'option_id{question.id}', None)
                user_id = self.request.user.id

                if option_id and user_id and question_id and poll_id:
                    my_object.append(Poll_Question_Responses(
                        poll_id=poll_id, question_id=question_id, option_id=option_id, user_id=user_id))

                else:
                    messages.error(
                        self.request, 'Response submission failed come back later')
                    log.error(
                        f'Response submission failed - Some values Are missing: (option: {option_id}) (user: {user_id}) (question: {question_id}) (poll: {poll_id})')
                    return redirect('index')
        else:
            messages.error(
                self.request, 'Response submission failed come back later')
            log.error('Response submission failed - No questions found')
            return redirect('index')

        Poll_Question_Responses.objects.bulk_create(my_object)
        messages.success(self.request, 'Response submitted successfully')
        log.info('Response submitted successfully')
        return redirect('index')


class DashboardsView(LoginRequiredMixin, TemplateView):
    template_name = 'website/dashboards.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardsView, self).get_context_data(**kwargs)
        context['options'] = Poll_Question_Responses.objects.select_related(
            'poll', 'question', 'option').values(
            'poll__title', 'question__question_text', 'option__option_text', 'option__id').annotate(votes=Count('option_id')).order_by('option_id')
        return context
