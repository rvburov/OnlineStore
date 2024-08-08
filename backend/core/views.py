from django.shortcuts import render


def page_not_found(request, exception):
    """Обрабатывает ошибки 404 (страница не найдена)."""
    return render(request, 'core/404.html', status=404)

def csrf_failure(request, reason=''):
    """Обрабатывает ошибки 403 (ошибка CSRF)."""
    return render(request, 'core/403csrf.html', status=403)

def server_error(request):
    """Обрабатывает ошибки 500 (внутренняя ошибка сервера)."""
    return render(request, 'core/500.html', status=500)

def bad_request(request, exception):
    """Обрабатывает ошибки 400 (плохой запрос)."""
    return render(request, 'core/400.html', status=400)
