from django.shortcuts import redirect

def verificar_rol(rol_requerido):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.userprofile.role == rol_requerido:
                return view_func(request, *args, **kwargs)
            return redirect('sin_permiso')
        return _wrapped_view
    return decorator
