from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            return redirect('/login/')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('/quiz/')

        return render(request, 'login.html', {
            'error': 'Invalid Username or Password'
        })

    return render(request, 'login.html')

from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('/logout/')