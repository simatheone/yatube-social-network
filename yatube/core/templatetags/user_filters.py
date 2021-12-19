from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    """
    Функиця возвращает кастомный фильтр, применяемый в шаблонах.
    """
    return field.as_widget(attrs={'class': css})
