from django.db import models
from django.utils import timezone


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
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='announcement', verbose_name='Категория')
    image = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name='Изображение')
    file = models.FileField(upload_to='news_files/', blank=True, null=True, verbose_name='Файл для скачивания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-date']


class Slide(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    image = models.ImageField(upload_to='slides/', verbose_name='Изображение для слайда')
    link = models.URLField(blank=True, null=True, verbose_name='Ссылка (если есть)')
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

    EDUCATION_LEVEL_CHOICES = [
        ('primary', 'Начальное общее образование (1-4 классы)'),
        ('secondary', 'Основное и/или среднее общее образование (5-11 классы)'),
        ('additional', 'Дополнительное образование детей и взрослых'),
        ('all', 'Все уровни образования'),
    ]

    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    photo = models.ImageField(upload_to='teachers/', verbose_name='Фото', blank=True, null=True)
    position = models.CharField(max_length=100, verbose_name='Должность')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='teacher', verbose_name='Роль')
    education_level = models.CharField(
        max_length=20,
        choices=EDUCATION_LEVEL_CHOICES,
        default='all',
        verbose_name='Уровень образовательной программы',
        help_text='Укажите, на каком уровне образования работает преподаватель'
    )
    bio = models.TextField(verbose_name='Дополнительная информация', blank=True, null=True,
                           help_text='Образование, достижения, стаж, награды и т.д.')

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
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Родительский раздел')
    title = models.CharField(max_length=200, verbose_name='Название раздела')
    slug = models.SlugField(unique=True, verbose_name='Ссылка (только латиницей)')
    content = models.TextField(verbose_name='Содержание', blank=True, help_text='Поддерживается HTML')
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