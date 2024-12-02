from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import logout, login, authenticate
from .models import UserProfile
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import PerfilForm


def register(request):
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = settings.DEFAULT_USER_ROLE
            profile.save()
            login(request, user)
            return redirect('Inicio') 
    else:
        user_creation_form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': user_creation_form})

def exit(request):
    logout(request)
    return redirect('login')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from cuentas.models import UserProfile

def iniciosesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                profile = UserProfile.objects.get(user=user)
                role = profile.role  

                request.session['perfil'] = role

                login(request, user)

                if role == 'Administrador':
                    return redirect('admin_dashboard')
                elif role == 'Supervisor':
                    return redirect('supervisor_dashboard')
                elif role == 'Vendedor':
                    return redirect('vendedor_dashboard')
                else:
                    return redirect('Inicio')

            except UserProfile.DoesNotExist:
                context = {
                    'error': 'Perfil de usuario no encontrado.'
                }
                return render(request, 'registration/login.html', context)
        else:
            context = {
                'error': 'Credenciales incorrectas. Intente nuevamente.'
            }
            return render(request, 'registration/login.html', context)

    return render(request, 'registration/login.html')


@login_required
def perfil(request):
    if request.method == "POST":
        form = PerfilForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Tu perfil ha sido actualizado correctamente.")
        elif password_form.is_valid():
            password_form.save()
            messages.success(request, "Tu contraseña ha sido cambiada correctamente.")
            return redirect('login')
    else:
        form = PerfilForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
    
    return render(request, 'registration/perfil.html', {
        'form': form,
        'password_form': password_form,
    })

def sin_permiso(request):
    return render(request, 'sin_permiso.html')