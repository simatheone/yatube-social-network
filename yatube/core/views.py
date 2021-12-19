from django.shortcuts import render


def page_not_found(request, exception):
    """
    Функция возвращает кастомную страницу для ошибки 404.
    """
    return render(request, 'core/404.html',
                  {'path': request.path}, status=404
                  )


def server_error(request):
    """
    Функция возвращает кастомную страницу для ошибки 500.
    """
    return render(request, 'core/500.html', status=500)


def permission_denied_view(request, exception):
    """
    Функция возвращает кастомную страницу для ошибки 403.
    """
    return render(request, 'core/403.html', status=403)
