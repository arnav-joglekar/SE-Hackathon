from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm,NoteShareForm
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required

@login_required(login_url='accounts:login')
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note, user=request.user)  # Pass the user
        if form.is_valid():
            note = form.save(commit=False)
            note.last_modified_by = request.user
            note.save()
            return redirect('notes:note_details', pk=note.pk)
    else:
        form = NoteForm(instance=note, user=request.user)  # Pass the user
    return render(request, 'notes/note_form.html', {'form': form})



@login_required(login_url='accounts:login')
def note_list(request):
    notes = Note.objects.filter(shared_with=request.user) | Note.objects.filter(created_by=request.user)
    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required(login_url='accounts:login')
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    shared_with = note.shared_with.all()
    return render(request, 'notes/note_details.html', {'note': note, 'shared_with': shared_with})

@login_required(login_url='accounts:login')
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.created_by = request.user
            note.save()
            # Add selected users to shared_with field
            users_to_share_with = form.cleaned_data.get('shared_with')
            if users_to_share_with:
                note.shared_with.add(*users_to_share_with)
            return redirect('notes:note_details', pk=note.pk)
    else:
        form = NoteForm(user=request.user)
    return render(request, 'notes/note_form.html', {'form': form})


@login_required(login_url='accounts:login')
def note_share(request, pk):
    note = get_object_or_404(Note, pk=pk)
 
    users_to_exclude = note.shared_with.all() | User.objects.filter(pk=request.user.pk)
    
    if request.method == 'POST':
        form = NoteShareForm(request.POST)
        if form.is_valid():
            users_to_share_with = form.cleaned_data['users']
            note.shared_with.add(*users_to_share_with)
            return redirect('notes:note_detail', pk=pk)
    else:
        # Initialize form with excluded users and allow multiple selections
        form = NoteShareForm(initial={'users': User.objects.exclude(pk__in=users_to_exclude)})
        form.fields['users'].widget.attrs['multiple'] = True
    
    return render(request, 'notes/note_share.html', {'form': form, 'note': note})

@login_required(login_url='accounts:login')
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('notes:note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})


