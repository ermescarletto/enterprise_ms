from django import forms
from django.template.loader import render_to_string


class DualListWidget(forms.Widget):
    template_name = "widgets/dual_list.html"

    def render(self, name, value, attrs=None, renderer=None):
        value = value or []
        selected_permissions = set(value) if isinstance(value, list) else set(value or [])

        # Criando as opções de permissão
        all_permissions = self.choices
        available_permissions = [perm for perm in all_permissions if perm[0] not in selected_permissions]
        selected_permissions_list = [perm for perm in all_permissions if perm[0] in selected_permissions]

        context = {
            "name": name,
            "available_permissions": available_permissions,
            "selected_permissions_list": selected_permissions_list,
        }

        return render_to_string(self.template_name, context)
