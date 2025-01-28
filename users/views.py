from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
# Create your views here.
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

User = get_user_model()

def logout_view(request):
    """Logs out the user and redirects to the login page."""
    logout(request)
    return redirect('users:login')

class CustomLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('cms:index')  # Replace 'home' with your app's home view name



@method_decorator(login_required, name='dispatch')
class UserListView(View):
    template_name = 'users/user_list.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # DataTables processa os dados no backend
        users = User.objects.all()
        data = []
        for user in users:
            ativo = ''
            if user.is_active:
                ativo = "<i class='bi bi-check-circle'></i>"
            else:
                ativo = "<i class='bi bi-dash-circle'></i>"
            data.append({
                "id": user.id,
                "nome": user.first_name,
                "email": user.email,
                "cpf": user.cpf,
                "ativo": ativo,
                "acoes": f"""
                <a href='/users/{user.id}/edit/' class='btn btn-primary btn-sm'><i class='bi bi-pen'></i></a>
                <a href='/users/{user.id}/delete/' class='btn btn-danger btn-sm'><i class='bi bi-trash'></i></a>
                """
            })
        return JsonResponse({"data": data})

from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserForm  # Crie um formulário customizado

class UserCreateView(CreateView):
    model = User
    template_name = 'users/user_form.html'
    form_class = UserForm
    success_url = reverse_lazy('users:list')

class UserUpdateView(UpdateView):
    model = User
    template_name = 'users/user_form.html'
    form_class = UserForm
    success_url = reverse_lazy('users:list')

from django.views.generic import DeleteView

class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:list')


from django.views import View

class ToggleActiveStatusView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.is_active = not user.is_active
        user.save()
        return JsonResponse({"status": "success", "is_active": user.is_active})
