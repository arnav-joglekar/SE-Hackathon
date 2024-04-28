from django import forms
from requests import request
from .models import Note
from django.contrib.auth.models import User
from django.db.models import Q


class NoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the current user
        super(NoteForm, self).__init__(*args, **kwargs)
        if user:
            # Exclude users who are already shared with this note or the current user
            self.fields['shared_with'].queryset = User.objects.exclude(
                Q(shared_notes__pk__in=[self.instance.pk]) | Q(pk=user.pk)
            )

    class Meta:
        model = Note
        fields = ['title', 'content', 'shared_with']



class NoteShareForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        note_instance = kwargs.pop('note_instance')
        super(NoteShareForm, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.exclude(pk__in=note_instance.shared_with.all())

    users = forms.ModelMultipleChoiceField(queryset=User.objects.none(), widget=forms.SelectMultiple)

    class Meta:
        model = Note
        fields = ['users']