from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import News, Slide, Teacher, Appeal, Section


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category', 'has_file', 'admin_thumbnail')
    list_filter = ('category', 'date')
    search_fields = ('title', 'text')
    list_per_page = 20
    date_hierarchy = 'date'

    def has_file(self, obj):
        return bool(obj.file)

    has_file.boolean = True
    has_file.short_description = 'Файл'

    def admin_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;"/>', obj.image.url)
        return "—"

    admin_thumbnail.short_description = 'Фото'


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'admin_thumbnail')
    list_editable = ('order',)

    def admin_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="50" style="object-fit: cover;"/>', obj.image.url)
        return "—"

    admin_thumbnail.short_description = 'Превью'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'role', 'subjects', 'total_experience', 'admin_thumbnail')
    list_filter = ('role',)
    search_fields = ('full_name', 'email', 'subjects')
    fieldsets = (
        ('Основная информация', {
            'fields': ('full_name', 'photo', 'position', 'role', 'subjects', 'education_programs')
        }),
        ('Образование и квалификация', {
            'fields': ('education_level', 'qualification', 'degree', 'academic_title')
        }),
        ('Опыт и стаж', {
            'fields': ('total_experience', 'teaching_experience')
        }),
        ('Повышение квалификации и переподготовка', {
            'fields': ('training_courses', 'retraining')
        }),
        ('Контактные данные и дополнительно', {
            'fields': ('email', 'phone', 'bio'),
            'classes': ('collapse',),
        }),
    )

    def admin_thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;"/>',
                               obj.photo.url)
        return "📷"

    admin_thumbnail.short_description = 'Фото'


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'subject', 'email', 'status', 'created_at', 'has_file')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'subject', 'message')
    list_editable = ('status',)
    readonly_fields = ('full_name', 'email', 'subject', 'message', 'file', 'created_at')
    date_hierarchy = 'created_at'
    list_per_page = 20

    def has_file(self, obj):
        return bool(obj.file)

    has_file.boolean = True
    has_file.short_description = 'Файл'


class ChildSectionInline(admin.TabularInline):
    model = Section
    fk_name = 'parent'
    extra = 1
    fields = ('title', 'slug', 'order', 'is_visible')
    prepopulated_fields = {'slug': ('title',)}
    verbose_name = 'Дочерний раздел'
    verbose_name_plural = 'Дочерние разделы'


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'order', 'is_visible')
    list_filter = ('parent', 'is_visible')
    search_fields = ('title', 'content')
    list_editable = ('order', 'is_visible')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ChildSectionInline]

    fieldsets = (
        ('Настройки раздела', {
            'fields': ('parent', 'title', 'slug', 'order', 'is_visible')
        }),
        ('Содержимое страницы', {
            'fields': ('content',),
            'description': 'Поддерживается HTML-разметка'
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if 'parent__id__exact' not in request.GET:
            qs = qs.filter(parent__isnull=True)
        return qs


admin.site.site_header = "Школа №141 - Панель управления"
admin.site.site_title = "Школа №141"
admin.site.index_title = "Добро пожаловать в систему управления сайтом"