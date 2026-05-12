from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import DocumentPage

from .models import (
    News,
    Slide,
    Teacher,
    Appeal,
    Section,
)

# ======================================================
# НАСТРОЙКА АДМИНКИ
# ======================================================

admin.site.site_header = "🏫 Школа №141 — Панель управления"
admin.site.site_title = "School141 Admin"
admin.site.index_title = "Управление школьным сайтом"


# ======================================================
# MIXIN ДЛЯ ПРЕВЬЮ КАРТИНОК
# ======================================================

class ImagePreviewMixin:

    @admin.display(description='Превью')
    def image_preview(self, obj):

        image = getattr(obj, 'image', None) or getattr(obj, 'photo', None)

        if image:
            return format_html(
                '''
                <img src="{}"
                style="
                    width:70px;
                    height:70px;
                    object-fit:cover;
                    border-radius:12px;
                    border:1px solid #d1d5db;
                    box-shadow:0 2px 6px rgba(0,0,0,.08);
                ">
                ''',
                image.url
            )

        return '—'


# ======================================================
# NEWS ADMIN
# ======================================================

@admin.register(News)
class NewsAdmin(ImagePreviewMixin, admin.ModelAdmin):

    list_display = (
        'title',
        'category_badge',
        'date',
        'has_image',
        'has_file',
        'image_preview',
    )

    list_filter = (
        'category',
        'date',
    )

    search_fields = (
        'title',
        'text',
    )

    ordering = ('-date',)

    date_hierarchy = 'date'

    save_on_top = True

    list_per_page = 20

    fieldsets = (

        (
            'Основная информация',
            {
                'fields': (
                    'title',
                    'category',
                    'date',
                )
            }
        ),

        (
            'Контент новости',
            {
                'fields': (
                    'text',
                    'image',
                    'file',
                )
            }
        ),
    )

    @admin.display(boolean=True, description='Фото')
    def has_image(self, obj):
        return bool(obj.image)

    @admin.display(boolean=True, description='Файл')
    def has_file(self, obj):
        return bool(obj.file)

    @admin.display(description='Категория')
    def category_badge(self, obj):

        colors = {
            'announcement': '#2563eb',
            'event': '#16a34a',
            'safety': '#dc2626',
            'exams': '#f59e0b',
        }

        labels = dict(News.CATEGORY_CHOICES)

        return format_html(
            '''
            <span style="
                background:{};
                color:white;
                padding:4px 10px;
                border-radius:999px;
                font-size:12px;
                font-weight:600;
            ">
                {}
            </span>
            ''',
            colors.get(obj.category, '#64748b'),
            labels.get(obj.category)
        )


# ======================================================
# SLIDES ADMIN
# ======================================================

@admin.register(Slide)
class SlideAdmin(ImagePreviewMixin, admin.ModelAdmin):

    list_display = (
        'title',
        'order',
        'image_preview',
    )

    list_editable = (
        'order',
    )

    ordering = ('order',)

    save_on_top = True

    fieldsets = (

        (
            'Слайд главной страницы',
            {
                'fields': (
                    'title',
                    'image',
                    'order',
                )
            }
        ),
    )


# ======================================================
# TEACHERS ADMIN
# ======================================================

@admin.register(Teacher)
class TeacherAdmin(ImagePreviewMixin, admin.ModelAdmin):

    list_display = (
        'full_name',
        'role_badge',
        'position',
        'subjects',
        'total_experience',
        'image_preview',
    )

    list_filter = (
        'role',
        'position',
    )

    search_fields = (
        'full_name',
        'position',
        'subjects',
        'email',
    )

    ordering = ('full_name',)

    save_on_top = True

    list_per_page = 30

    fieldsets = (

        (
            'Основная информация',
            {
                'fields': (
                    'full_name',
                    'photo',
                    'role',
                    'position',
                    'subjects',
                )
            }
        ),

        (
            'Контакты',
            {
                'fields': (
                    'email',
                    'phone',
                )
            }
        ),

        (
            'Образование',
            {
                'classes': ('collapse',),
                'fields': (
                    'education_level',
                    'qualification',
                    'degree',
                    'academic_title',
                )
            }
        ),

        (
            'Стаж',
            {
                'fields': (
                    'total_experience',
                    'teaching_experience',
                )
            }
        ),

        (
            'Курсы и переподготовка',
            {
                'classes': ('collapse',),
                'fields': (
                    'training_courses',
                    'retraining',
                )
            }
        ),

        (
            'Дополнительная информация',
            {
                'classes': ('collapse',),
                'fields': (
                    'education_programs',
                    'bio',
                )
            }
        ),
    )

    @admin.display(description='Роль')
    def role_badge(self, obj):

        colors = {
            'director': '#dc2626',
            'deputy': '#f59e0b',
            'teacher': '#2563eb',
        }

        labels = dict(Teacher.ROLE_CHOICES)

        return format_html(
            '''
            <span style="
                background:{};
                color:white;
                padding:4px 10px;
                border-radius:999px;
                font-size:12px;
                font-weight:600;
            ">
                {}
            </span>
            ''',
            colors.get(obj.role, '#64748b'),
            labels.get(obj.role)
        )


# ======================================================
# APPEALS ADMIN
# ======================================================

@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'subject',
        'status_badge',
        'created_at',
        'has_file',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'full_name',
        'email',
        'subject',
        'message',
    )

    readonly_fields = (
        'created_at',
    )

    date_hierarchy = 'created_at'

    ordering = ('-created_at',)

    save_on_top = True

    fieldsets = (

        (
            'Обращение',
            {
                'fields': (
                    'full_name',
                    'email',
                    'subject',
                    'message',
                    'file',
                    'status',
                    'created_at',
                )
            }
        ),
    )

    @admin.display(boolean=True, description='Файл')
    def has_file(self, obj):
        return bool(obj.file)

    @admin.display(description='Статус')
    def status_badge(self, obj):

        colors = {
            'new': '#dc2626',
            'considered': '#f59e0b',
            'answered': '#16a34a',
        }

        labels = dict(Appeal.STATUS_CHOICES)

        return format_html(
            '''
            <span style="
                background:{};
                color:white;
                padding:4px 10px;
                border-radius:999px;
                font-size:12px;
                font-weight:600;
            ">
                {}
            </span>
            ''',
            colors.get(obj.status, '#64748b'),
            labels.get(obj.status)
        )


# ======================================================
# INLINE ДЛЯ ДОЧЕРНИХ РАЗДЕЛОВ
# ======================================================

class ChildSectionInline(admin.StackedInline):

    model = Section

    fk_name = 'parent'

    extra = 0

    show_change_link = True

    classes = ('collapse',)

    fields = (
        'title',
        'slug',
        'order',
        'is_visible',
        'content',
    )

    prepopulated_fields = {
        'slug': ('title',)
    }

    verbose_name = 'Подраздел'

    verbose_name_plural = 'Дочерние подразделы'


# ======================================================
# SECTION ADMIN
# ======================================================

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):

    list_display = (
        'tree_title',
        'parent',
        'order',
        'is_visible',
        'children_count',
        'site_link',
    )

    list_filter = (
        'is_visible',
        'parent',
    )

    search_fields = (
        'title',
        'content',
    )

    list_editable = (
        'order',
        'is_visible',
    )

    ordering = (
        'parent__id',
        'order',
        'title',
    )

    save_on_top = True

    inlines = [ChildSectionInline]

    prepopulated_fields = {
        'slug': ('title',)
    }

    fieldsets = (

        (
            'Раздел сайта',
            {
                'fields': (
                    'parent',
                    'title',
                    'slug',
                    'order',
                    'is_visible',
                )
            }
        ),

        (
            'Содержимое страницы',
            {
                'fields': (
                    'content',
                ),
                'description': 'Можно использовать HTML'
            }
        ),
    )

    @admin.display(description='Раздел')
    def tree_title(self, obj):

        level = 0
        parent = obj.parent

        while parent:
            level += 1
            parent = parent.parent

        return mark_safe(
            '&nbsp;&nbsp;&nbsp;&nbsp;' * level +
            ('↳ ' if level else '') +
            f'<strong>{obj.title}</strong>'
        )

    @admin.display(description='Подразделов')
    def children_count(self, obj):

        return obj.section_set.count()

    @admin.display(description='Сайт')
    def site_link(self, obj):

        return format_html(
            '''
            <a href="{}"
            target="_blank"
            style="
                padding:6px 10px;
                background:#2563eb;
                color:white;
                border-radius:8px;
                text-decoration:none;
                font-weight:600;
            ">
                Открыть
            </a>
            ''',
            obj.get_absolute_url()
        )

@admin.register(DocumentPage)
class DocumentPageAdmin(admin.ModelAdmin):
    # Показываем только один объект — с slug='documents'
    list_display = ('title', 'is_visible', 'site_link')
    fields = ('title', 'slug', 'content', 'is_visible')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(slug='documents')

    # Запрещаем удаление и создание новых объектов (только редактирование существующего)
    def has_add_permission(self, request):
        return not self.model.objects.filter(slug='documents').exists()

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description='Сайт')
    def site_link(self, obj):
        return format_html('<a href="{}" target="_blank">Открыть</a>', obj.get_absolute_url())