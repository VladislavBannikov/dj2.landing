from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    if 'from-landing' in request.GET:
        counter_click.update([request.GET.get('from-landing')])
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов

    # не понятно, что делать если параметра нет. В задании это явно не указано.
    page_name = "index.html"
    if 'ab-test-arg' in request.GET:
        ab_test = request.GET.get('ab-test-arg').lower()
        if ab_test == 'test':
            page_name = 'landing_alternate.html'
        elif ab_test == 'original':
            page_name = 'landing.html'
        else:
            # не понятно, что делать если параметр не test или original.
            pass
        counter_show.update([ab_test])

    return render_to_response(page_name)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    test_conversion = str(counter_click['test'] / counter_show['test']) if counter_show['test'] else "Нет статистики"
    original_conversion = str(counter_click['original'] / counter_show['original']) if counter_show[
        'original'] else "Нет статистики"
    return render_to_response('stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
