from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True, null=False)
    end_date = models.DateTimeField(auto_now_add=True, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.title


class Poll_Questions(models.Model):
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.question_text


class Poll_Question_Options(models.Model):
    question = models.ForeignKey(
        Poll_Questions, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.option_text


class Poll_Question_Responses(models.Model):
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Poll_Questions, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
    )
    option = models.ForeignKey(
        Poll_Question_Options, on_delete=models.CASCADE, related_name='responses')

    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.option.option_text
