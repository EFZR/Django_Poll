from django import forms
from .models import Poll, Poll_Questions, Poll_Question_Options


class PollForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Poll Title'}),
    )

    class Meta:
        model = Poll
        fields = ['title',]


class Poll_Questions_Form(forms.ModelForm):
    
    question_text = forms.CharField(
        max_length=100,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Add a new Query'}),
    )

    class Meta:
        model = Poll_Questions
        fields = ['question_text']


class Poll_Questions_Options_Form(forms.ModelForm):
    option_text = forms.CharField(
        max_length=100,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Option'}),
    )

    class Meta:
        model = Poll_Question_Options
        fields = ['option_text']
