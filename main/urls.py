from django.urls import path
from . import views

urlpatterns = [
    # Главные страницы
    path('', views.index_view, name='index'),
    path('parents/', views.parents_view, name='parents'),
    path('news/', views.news_list_view, name='news_list'),
    path('news/<int:pk>/', views.news_detail_view, name='news_detail'),
    path('teachers/', views.teachers_list_view, name='teachers_list'),
    path('teachers/<int:pk>/', views.teacher_detail_view, name='teacher_detail'),
    path('appeal/', views.appeal_view, name='appeal'),
    path('documents/', views.documents_view, name='documents'),
    path('info/bezopasnost/', views.section_detail_view, {'slug': 'bezopasnost'}, name='info_bezopasnost'),
    path('info/gia/', views.section_detail_view, {'slug': 'gia'}, name='info_gia'),
    path('search/', views.search_view, name='search'),

    # Страницы документов
    path('documents/vpr/', views.vpr_view, name='vpr'),
    path('documents/gto/', views.gto_view, name='gto'),
    path('documents/health/', views.health_view, name='health'),

    # Разделы "Сведения об ОО" (все управляется через админку)
    path('info/', views.info_index_view, name='info_index'),
    path('info/<slug:slug>/', views.section_detail_view, name='section_detail'),
]