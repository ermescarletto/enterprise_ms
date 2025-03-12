from django.shortcuts import render
from .serializers import *
from django.db.models import ProtectedError
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView, BSModalUpdateView, BSModalDeleteView
from django.views import View
from .forms import *
from .models import *
from .serializers import *
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

class BaseListView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    def has_model_permission(self, model):
        """
        Verifica se o usuário tem permissão para uma ação em um modelo.
        :param model: Modelo para verificar as permissões
        :return: True se o usuário tiver permissão, False caso contrário
        """
        add = self.request.user.has_perm('add', model._meta.model_name)
        change = self.request.user.has_perm('change', model._meta.model_name)
        delete = self.request.user.has_perm('delete', model._meta.model_name)
        view = self.request.user.has_perm('view', model._meta.model_name)

        return [view, add, change, delete]


class BaseCreateView(LoginRequiredMixin, BSModalCreateView):
    login_url = '/user/login/'
    template_name = 'generics/form.html'


#### VIEWS DO CADASTRO DE CIDADES #### 26/02/2025
#### TRILHA SONORA "LAS TUMBAS - ISRAEL RIVERA" #####


class CidadeListView(BaseListView):
    def get(self, request):
        user_perms = self.has_model_permission(Cidade)
        context = {
            'page_title': Cidade.get_model_name(Cidade),
            'url_create': 'cadastros:create-cidade',
            'url_view': 'cadastros:view-cidade',
            'url_edit': 'cadastros:edit-cidade',
            'url_delete': 'cadastros:delete-cidade',
            'user_perms': user_perms
        }
        return render(request, "generics/list.html", context=context)



#### VIES DO CADASTRO DE EMPRESAS #####

class Empresa(BaseCreateView):
    form_class = FormEmpresa
    success_message = 'Empresa criada com sucesso.'
    error_message = 'Não foi possível cadastrar.'
    success_url = reverse_lazy('cadastros:empresa')


class EmpresaDetail(LoginRequiredMixin, BSModalReadView):
    template_name = 'generics/detail.html'
    model = Empresa


class EmpresaEditView(LoginRequiredMixin, BSModalUpdateView):
    model = Empresa
    template_name = 'generics/edit.html'
    form_class = FormEmpresa
    success_message = 'Empresa editada com sucesso'
    success_url = reverse_lazy('cadastros:empresa')


class EmpresaDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Empresa
    template_name = 'generics/delete.html'
    success_message = 'Empresa removida com sucesso.'
    success_url = reverse_lazy('cadastros:empresa')
    error_url = reverse_lazy('cadastros:empresa')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(request, "Não foi possível excluir o registro.")
        finally:
            return HttpResponseRedirect(success_url)


class Empresa(BaseListView):
    def get(self, request):
        user_perms = self.has_model_permission(Empresa)
        objects = Empresa.objects.all().order_by('id')
        context = {
            'objects': objects,
            'page_title': Empresa.get_model_name(Empresa),
            'url_create': 'frotas:create_transportador',
            'url_view': 'frotas:view_transportador',
            'url_edit': 'frotas:edit_transportador',
            'url_delete': 'frotas:delete_transportador',
            'user_perms': user_perms
        }
        return render(request, "generics/list.html", context=context)


class EmpresaListView(LoginRequiredMixin,View):
    template_name = 'groups/empresa_list.html'
    def get(self, request):
        # DataTables processa os dados no backend
        groups = Empresa.objects.all()
        data = []
        for group in groups:
            data.append({
                "id": empresa.id,
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

