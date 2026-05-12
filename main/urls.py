from django.urls import path
from . import views

urlpatterns = [
    # Главные страницы
    path('', views.index_view, name='index'),
    path('news/', views.news_list_view, name='news_list'),
    path('news/<int:pk>/', views.news_detail_view, name='news_detail'),
    path('teachers/', views.teachers_list_view, name='teachers_list'),
    path('teachers/<int:pk>/', views.teacher_detail_view, name='teacher_detail'),
    path('appeal/', views.appeal_view, name='appeal'),

    # Страницы документов (подразделы)
    path('documents/vpr/', views.vpr_view, name='vpr'),
    path('documents/gto/', views.gto_view, name='gto'),
    path('documents/health/', views.health_view, name='health'),

    # Поиск
    path('search/', views.search_view, name='search'),

    # Разделы "Сведения об ОО"
    path('info/', views.info_index_view, name='info_index'),
    path('info/<slug:slug>/', views.section_detail_view, name='section_detail'),

    # !!! Новый маршрут для страницы Документов (псевдоним 'documents')
    path('documents/', views.section_detail_view, {'slug': 'documents'}, name='documents'),
]