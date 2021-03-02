from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as do_login, logout as do_logout


from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
from .models import *
from covid19.forms import CreateUserForm


def index(request):
    print(request.user.is_authenticated)
    return render(request, 'index.html', {'user': request.user})


def welcome(request):
    if request.user.is_authenticated:
        return render(request, "templates/index.html")
    return redirect('/login')


def register(request):
    # We create empty authentication form
    form = CreateUserForm()
    if request.method == "POST":
        # Add receive data to rhe form
        form = CreateUserForm(request.POST)

        # If the form is valied...
        if form.is_valid():

            # We create a new user account
            user = form.save()
            newname = form.cleaned_data.get('username')
            messages.success(request, 'El usuario ' + newname +
                             ' ha sido registrada con éxito')
            # If the user is create correctly
            if user is not None:
                # We make the manual login
                do_login(request, user)
                # And we redirect to the cover
                return redirect('/login')

    # Delete helper texts
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None
    # If we reach to the end we render the form
    return render(request, "register.html", {'form': form})


def login(request):

    form = AuthenticationForm()
    if request.method == "POST":
        # Add data received to the form
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                # Doing the manual login
                do_login(request, user)
                return redirect('/dashboard')

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form': form})


def dashboard(request):
    # if request.user.is_authenticated:
    return render(request, "dashboard.html")


def logout(request):
    do_logout(request)
    return redirect('/')
