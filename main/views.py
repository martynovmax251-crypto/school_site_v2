from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import News, Slide, Teacher, Appeal, Section


def index_view(request):
    """Главная страница"""
    slides = Slide.objects.all()
    news = News.objects.all()[:6]
    director = Teacher.objects.filter(role='director').first()

    context = {
        'slides': slides,
        'news': news,
        'director': director,
    }
    return render(request, 'main/index.html', context)


def news_list_view(request):
    """Страница со списком новостей"""
    news_list = News.objects.all()

    category = request.GET.get('category')
    if category:
        news_list = news_list.filter(category=category)

    search_query = request.GET.get('search')
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) |
            Q(text__icontains=search_query)
        )

    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'current_category': category,
        'search_query': search_query,
    }
    return render(request, 'main/news_list.html', context)


def news_detail_view(request, pk):
    """Детальная страница новости"""
    news = get_object_or_404(News, pk=pk)
    return render(request, 'main/news_detail.html', {'news': news})


def teachers_list_view(request):
    """Страница со списком учителей"""
    director = Teacher.objects.filter(role='director').first()
    deputies = Teacher.objects.filter(role='deputy')
    teachers = Teacher.objects.filter(role='teacher')

    group_by = request.GET.get('group')

    context = {
        'director': director,
        'deputies': deputies,
        'teachers': teachers,
        'group_by': group_by,
    }
    return render(request, 'main/teachers_list.html', context)


def teacher_detail_view(request, pk):
    """Детальная страница учителя"""
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'main/teacher_detail.html', {'teacher': teacher})


def appeal_view(request):
    """Страница с формой обращений"""
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        file = request.FILES.get('file')

        appeal = Appeal.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message,
            file=file
        )

        messages.success(request, 'Ваше обращение успешно отправлено!')
        return redirect('appeal')

    return render(request, 'main/appeal_form.html')


def documents_view(request):
    """Главная страница документов"""
    return render(request, 'main/documents.html')


def vpr_view(request):
    """Страница ВПР 2026"""
    return render(request, 'main/vpr.html')


def gto_view(request):
    """Страница ГТО 95 лет"""
    return render(request, 'main/gto.html')


def health_view(request):
    """Страница профилактики клещей / ЗОЖ"""
    return render(request, 'main/health.html')


# =================================================================
# РАЗДЕЛЫ (управляются через админку, модель Section)
# =================================================================

def info_index_view(request):
    """Главная страница раздела Сведения об ОО — только родительские разделы"""
    sections = Section.objects.filter(parent__isnull=True, is_visible=True)
    return render(request, 'main/info/index.html', {'sections': sections})

def section_detail_view(request, slug):
    """Страница раздела — показывает содержимое и дочерние разделы"""
    section = get_object_or_404(Section, slug=slug, is_visible=True)
    return render(request, 'main/section_detail.html', {'section': section})


# ========== ОБРАБОТЧИКИ ОШИБОК ==========

def handler404(request, exception):
    """Страница 404 - не найдено"""
    return render(request, '404.html', status=404)


def handler500(request):
    """Страница 500 - ошибка сервера"""
    return render(request, '500.html', status=500)


def handler403(request, exception):
    """Страница 403 - доступ запрещен"""
    return render(request, '403.html', status=403)