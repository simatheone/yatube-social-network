from datetime import datetime as dt


def year(request):
    """
    Функция, которая возвращает текущий год.
    """
    current_year = int(dt.now().strftime('%Y'))
    return {
        'year': current_year,
    }
