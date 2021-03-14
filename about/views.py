from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/simple_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Об авторе'
        context['text'] = 'Информация об авторе'
        return context


class AboutTechView(TemplateView):
    template_name = 'about/simple_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Технологии'
        context['text'] = 'Тут описаны технологии'
        return context
