from django import forms
from django.forms import inlineformset_factory
from post.models import Post, PostImage, Comment
from utils.forms import BootstrapModelForm



class PostForm(BootstrapModelForm):
    class Meta:
        model = Post
        fields = ('content',)

class PostImageForm(BootstrapModelForm):
    class Meta:
        model = PostImage
        fields = ('image',)

PostImageFormSet = inlineformset_factory(
    Post, PostImage, form=PostImageForm, extra=1, can_delete=True
)

class CommentForm(BootstrapModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
