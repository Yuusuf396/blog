from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        # exclude=["post"]
        fields = ['user_name', 'user_email', 'text']
        # include="__all__"
        labels={
            "user_name":"Your Name",
            "user_email":"Your Email",
            "text":"Your Comment"
        }