from .models import Profissionaldasaude, Administrativo

def user_info(request):
    user = request.user
    context = {
        'user': user,
        'profissional_saude': None,
        'administrativo': None,
    }

    if user.is_authenticated:
        try:
            context['profissional_saude'] = Profissionaldasaude.objects.get(usuario=user)
        except Profissionaldasaude.DoesNotExist:
            pass

        try:
            context['administrativo'] = Administrativo.objects.get(usuario=user)
        except Administrativo.DoesNotExist:
            pass

    return context