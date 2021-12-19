from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """
    View-класс для отоброжения статичной страницы "об авторе".
    """
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        """
        Функиця, которая переоределяет значение 'title' в родительском
        классе 'TemplateView'.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Об авторе'
        return context


class AboutTechView(TemplateView):
    """
    View-класс для отоброжения статичной страницы "технологии".
    """

    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        """
        Функиця, которая переоределяет значение 'title' в родительском
        классе 'TemplateView'.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Технологии проекта'
        return context
