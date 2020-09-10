from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from profiles.forms import LoginForm, RegisterForm, ChangeForm
from django.contrib.auth.models import User
from profiles.models import Profile

from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                profile = Profile.objects.get(
                    user=User.objects.get(username=form.cleaned_data.get('username')))
                profile.bio = form.cleaned_data.get('bio')
                profile.save()
                return redirect('login')

        context = {"form": form, "form_title": "Registration",
                   "form_button": "Register"}
        return render(request, 'profiles/register.html', context)


def login_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = LoginForm()
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                context['error'] = "Wrong password or username"
        context['form'] = form
        return render(request, 'profiles/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def index(request):
    return render(request, "profiles/index.html", {"users": User.objects.all()})


@login_required(login_url="login")
def change_view(request, user_id):
    if request.method == 'POST':
        print("I'm in POST CHANGE VIEW")
        form = ChangeForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=user_id)
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.email = form.cleaned_data.get("email")
            user.profile.bio = form.cleaned_data.get("bio")
            user.save()
            return redirect('index')

    user = User.objects.get(pk=user_id)
    initial_data = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "bio": user.profile.bio
    }

    print(f"INITIAL_DATA: {initial_data}")
    form = ChangeForm(initial=initial_data)
    return render(request, "profiles/change.html", context={"form": form, "user_id": user_id})


@login_required(login_url="login")
def delete_view(request, user_id):
    User.objects.filter(pk=user_id).delete()
    return redirect("index")
