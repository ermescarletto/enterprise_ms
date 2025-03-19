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
from django.http import JsonResponse

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
#### REFATORADO EM 18/03 PARA ATENDER O TEMPLATE DO DJANGO ####

class CidadeListView(LoginRequiredMixin,View):
    template_name = 'cidades/cidade_list.html'

    def get(self, request):
        return render(request, self.template_name)
class GetCidadesListView(LoginRequiredMixin,View):
    def get(self, request):
        cidades = Cidade.objects.all()
        data = []
        for cidade in cidades:
            data.append({
                "id": cidade.id,
                "nome": cidade.nome,
                "estado": cidade.estado,
                "cep_de": cidade.cep_de,
                "cep_ate": cidade.cep_ate,
                "acoes": f"""
                <a href='{cidade.id}/edit/' class='btn btn-primary btn-sm'><i class='bi bi-pen edit'></i></a>
                <a href='{cidade.id}/delete/' class='btn btn-danger btn-sm'><i class='bi bi-trash'></i></a>
                """
            })
        return JsonResponse({"data": data})

####### VIEWS DE PESSOA JURIDICA ######
#### 18/03/2025 - Rumo ao Caiaque ######


class PessoaJuridicaListView(LoginRequiredMixin,View):
    template_name = 'pessoajuridica/pessoa_juridica_list.html'

    def get(self, request):
        return render(request, self.template_name)
class GetPessoaJuridicaListView(LoginRequiredMixin,View):
    def get(self, request):
        pessoajuridicas = PessoaJuridica.objects.all()
        data = []
        for pessoa in pessoajuridicas:
            data.append({
                "id": pessoa.id,
                "nome_fantasia": pessoa.nome_fantasia,
                "razao_social": pessoa.razao_social,
                "cnpj" : pessoa.cnpj,
                "inscricao_estadual" : pessoa.inscricao_estadual,
                "inscricao_municipal" : pessoa.inscricao_municipal,
                "email" : pessoa.email,
                "telefone" : pessoa.telefone,
                "acoes": f"""
                <a href='{pessoa.id}/edit/' class='btn btn-primary btn-sm'><i class='bi bi-pen edit'></i></a>
                <a href='{pessoa.id}/delete/' class='btn btn-danger btn-sm'><i class='bi bi-trash'></i></a>
                """
            })
        return JsonResponse({"data": data})



####### VIEWS DE UNIDADE ######
#### 18/03/2025 - Continua rumo ao caiaque ######


class UnidadeListView(LoginRequiredMixin,View):
    template_name = 'unidade/unidade_list.html'

    def get(self, request):
        return render(request, self.template_name)
class GetUnidadesListView(LoginRequiredMixin,View):
    def get(self, request):
        unidades = Unidade.objects.all()
        data = []
        for unidade in unidades:
            data.append({
                "id": unidade.id,
                "codigo": unidade.codigo,
                "nome": unidade.nome,
                "cnpj" : unidade.cnpj,
                "empresa" : unidade.empresa.razao_social,
                "ativo" : unidade.ativo,
                "acoes": f"""
                <a href='{unidade.id}/edit/' class='btn btn-primary btn-sm'><i class='bi bi-pen edit'></i></a>
                <a href='{unidade.id}/delete/' class='btn btn-danger btn-sm'><i class='bi bi-trash'></i></a>
                """
            })
        return JsonResponse({"data": data})



###### VIEWS DO CADASTRO DE GERENTE ########
###### I NEED MONEY ##### LETS CODE ######
###### NO IA NEEDED IN THIS SHIT ###########



class GerenteListView(LoginRequiredMixin,View):
    template_name = 'gerente/gerente_list.html'

    def get(self, request):
        return render(request, self.template_name)
class GetGerentesListView(LoginRequiredMixin,View):
    def get(self, request):
        gerentes = Gerente.objects.all()
        data = []
        for gerente in gerentes:
            data.append({
                "id": gerente.id,
                "usuario": '{} {}'.format(gerente.usuario.first_name,gerente.usuario.last_name),
                "unidades": gerente.unidades.nome,
                "ativo" : gerente.ativo,
                "acoes": f"""
                <a href='{gerente.id}/edit/' class='btn btn-primary btn-sm'><i class='bi bi-pen edit'></i></a>
                <a href='{gerente.id}/delete/' class='btn btn-danger btn-sm'><i class='bi bi-trash'></i></a>
                """
            })
        return JsonResponse({"data": data})

