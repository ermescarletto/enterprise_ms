from django import forms
from django.template.loader import render_to_string


class DualListWidget(forms.Widget):
    template_name = "widgets/dual_list.html"
    def render(self, name, value, attrs=None, renderer=None):
        value = value or []
        selected = set(value) if isinstance(value, list) else set(value or [])

        # Criando as opções de permissão
        all = self.choices
        available = [perm for perm in all if perm[0] not in selected]
        selected = [perm for perm in all if perm[0] in selected]

        context = {
            "name": name,
            "available": available,
            "selected": selected,
        }

        return render_to_string(self.template_name, context)
