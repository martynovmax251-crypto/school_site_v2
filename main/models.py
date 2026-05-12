from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField
from django_ckeditor_5.fields import CKEditor5Field


class News(models.Model):
    CATEGORY_CHOICES = [
        ('announcement', 'Объявления'),
        ('event', 'Мероприятия'),
        ('safety', 'Профилактика'),
        ('exams', 'ВПР/ГТО'),
    ]

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='announcement',
                                verbose_name='Категория')
    image = ResizedImageField(
        size=[800, 450],
        crop=['middle', 'center'],
        quality=85,
        upload_to='news_images/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    file = models.FileField(upload_to='news_files/', blank=True, null=True, verbose_name='Файл для скачивания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date']


class Slide(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    image = ResizedImageField(
        size=[1920, 800],
        crop=['middle', 'center'],
        quality=85,
        upload_to='slides/',
        blank=True,
        null=True,
        verbose_name='Изображение для слайда'
    )
    order = models.IntegerField(default=0, verbose_name='Порядок')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


class Teacher(models.Model):
    ROLE_CHOICES = [
        ('director', 'Директор'),
        ('deputy', 'Завуч'),
        ('teacher', 'Учитель'),
    ]

    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    photo = ResizedImageField(
        size=[600, 800],
        crop=['middle', 'center'],
        quality=85,
        upload_to='teachers/',
        blank=True,
        null=True,
        verbose_name='Фото'
    )
    position = models.CharField(max_length=100, verbose_name='Должность')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='teacher', verbose_name='Роль')
    bio = models.TextField(verbose_name='Дополнительная информация', blank=True, null=True)

    # Новые поля по требованиям
    subjects = models.CharField(max_length=300, blank=True, null=True, verbose_name='Преподаваемые предметы')
    education_level = models.CharField(max_length=500, blank=True, null=True,
                                       verbose_name='Уровень образования (диплом)')
    qualification = models.CharField(max_length=200, blank=True, null=True, verbose_name='Квалификация по диплому')
    degree = models.CharField(max_length=200, blank=True, null=True, verbose_name='Учёная степень (при наличии)')
    academic_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Учёное звание (при наличии)')
    training_courses = models.TextField(blank=True, null=True,
                                        verbose_name='Повышение квалификации за последние 3 года')
    retraining = models.TextField(blank=True, null=True, verbose_name='Профессиональная переподготовка')
    total_experience = models.IntegerField(default=0, verbose_name='Общий стаж работы (лет)')
    teaching_experience = models.IntegerField(default=0, verbose_name='Педагогический стаж (лет)')
    education_programs = models.CharField(max_length=500, blank=True, null=True,
                                          verbose_name='Образовательные программы (какие классы)')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Appeal(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('considered', 'Рассмотрено'),
        ('answered', 'Отвечено'),
    ]

    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    file = models.FileField(upload_to='appeals/', blank=True, null=True, verbose_name='Файл')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.subject} - {self.full_name}'

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        ordering = ['-created_at']


class Section(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Родительский раздел')
    title = models.CharField(max_length=200, verbose_name='Название раздела')
    slug = models.SlugField(unique=True, verbose_name='Ссылка (только латиницей)')
    content = CKEditor5Field(verbose_name='Содержание', blank=True)
    order = models.IntegerField(default=0, verbose_name='Порядок')
    is_visible = models.BooleanField(default=True, verbose_name='Показывать на сайте')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы (Сведения об ОО)'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/info/{self.slug}/'


class DocumentPage(Section):
    class Meta:
        proxy = True
        verbose_name = 'Документы'
        verbose_name_plural = 'Документы'