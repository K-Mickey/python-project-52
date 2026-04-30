from django.shortcuts import render
from django.utils.translation import gettext_lazy
from django.views import View


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        context = {"page_title": gettext_lazy("Task manager")}
        return render(request, self.template_name, context)
