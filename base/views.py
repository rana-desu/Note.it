from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from multiprocessing import AuthenticationError

from .models import Note, Topic
from .forms import NoteForm

# function for login and registration
def loginPage(request):

    page = 'login'
     
    if request.user.is_authenticated:
        return redirect('home')

    
    # getting the users' credentials 
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # checking if username exists
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        # authorizing the users' credentials 
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not exist.')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm (request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save() 
            login(request, user)
            return redirect('home')

    return render(request, 'base/login_register.html', {'form': form})



# function for basic home page
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # searching parameters
    notes = Note.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    note_count = notes.count()
    topics = Topic.objects.all()
    context = {'notes': notes, 'topics': topics, 'note_count': note_count}
    return render(request, 'base/home.html', context)


# function for displaying notes
def note(request, pk):
    note = Note.objects.get(id=pk)
    context = {'note': note}
    return render(request, 'base/note.html', context)


@login_required(login_url='login')
# function for creating a note
def createNote(request):
    form = NoteForm()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/note_form.html', context)


@login_required(login_url='login')
# function for updating a note 
def updateNote(request, pk):
    note = Note.objects.get(id=pk)
    form = NoteForm(instance=note)

    # checking if the user is the owner of note
    if request.user != note.host:
        return HttpResponse("You're not allowed to update/edit this note.")

    # form for updating a note
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/note_form.html', context)


@login_required(login_url='login')
# function for deleting a note
def deleteNote(request, pk):

    note = Note.objects.get(id=pk)

    if request.method == 'POST':
        note.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': note})
