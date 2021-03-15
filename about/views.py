from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/simple_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Об авторе'
        context[
            'text'] = 'Дипломный проект Воронова Д.С., github.com/crablind1'
        return context


class AboutTechView(TemplateView):
    template_name = 'about/simple_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Технологии'
        context['text'] = 'Стэк - Django, Gunicorn, Nginx, PostgreSQL, Docker'
        return context
