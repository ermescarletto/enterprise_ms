from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
# Create your views here.
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import View, CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from bootstrap_modal_forms.mixins import PassRequestMixin, CreateUpdateAjaxMixin

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

class UserListView(LoginRequiredMixin,View):
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
                <a href='{user.id}/edit/' class='btn btn-primary btn-sm'><i class='bi bi-pen edit'></i></a>
                <a href='{user.id}/delete/' class='btn btn-danger btn-sm'><i class='bi bi-trash'></i></a>
                """
            })
        return JsonResponse({"data": data})


class GetUsersView(LoginRequiredMixin,View):
    def get(self, request):
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
                <a href='{user.id}/edit/' class='btn btn-primary btn-sm'><i class='bi bi-pen edit'></i></a>
                <a href='{user.id}/delete/' class='btn btn-danger btn-sm'><i class='bi bi-trash'></i></a>
                """
            })
        return JsonResponse({"data": data})


class GroupListView(LoginRequiredMixin,View):
    template_name = 'groups/empresa_list.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # DataTables processa os dados no backend
        groups = Group.objects.all()
        data = []
        for group in groups:
            data.append({
                "id": group.id,
                "nome": group.name,
                "acoes" :  f"""
                <button 
                    type="button" 
                    class="edit bs-modal btn btn-sm btn-secondary"     
                    data-bs-toggle="modal" 
                    data-bs-target="#modal"  
                    data-form-url='groups/{group.id}/edit/'
                >
                <span class="bi bi-pen"></span>
                </button>               
                <a href='{group.id}/edit/' class='btn btn-primary btn-sm'><i class='bi bi-pen'></i></a>
                <a href='{group.id}/delete/' class='btn btn-danger btn-sm'><i class='bi bi-trash'></i></a>
                """
            })
        return JsonResponse({"data": data})


class UserCreateView(BSModalCreateView):
    template_name = 'users/user_form.html'
    form_class = UserModalForm
    success_message = 'Usuário criado com sucesso'
    success_url = reverse_lazy('users:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            return JsonResponse({
                'success': True,
                'message': self.success_message,
                'redirect_url': self.get_success_url()
            })
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return response


class GroupCreateView(BSModalCreateView):
    template_name = 'groups/empresa_form.html'
    form_class = GroupModalForm
    success_message = 'Grupo criado com sucesso'
    success_url = reverse_lazy('users:groups')

class UserUpdateView(UpdateView):
    model = User
    template_name = 'users/empresa_form.html'
    form_class = UserForm
    success_url = reverse_lazy('users:list')



class GroupEditView(BSModalUpdateView):
    model = Group
    template_name = 'groups/empresa_edit.html'
    form_class = GroupEditForm
    success_url = reverse_lazy('users:groups')


from django.views.generic import DeleteView

class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:list')
class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'groups/group_confirm_delete.html'
    success_url = reverse_lazy('users:groups')


from django.views import View

class ToggleActiveStatusView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.is_active = not user.is_active
        user.save()
        return JsonResponse({"status": "success", "is_active": user.is_active})
