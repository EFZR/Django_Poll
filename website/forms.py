from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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
        fields = ['title', 'is_active']


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


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Username'}),
    )
    password = forms.CharField(
        max_length=100,
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Password'}),
    )


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    email = forms.EmailField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'E-Mail'}),
    )
    first_name = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Last Name'}),
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )
