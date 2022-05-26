from django import forms

from blog.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['created_at', 'post', 'name', 'email', ]
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Комментарий'}),
        }
