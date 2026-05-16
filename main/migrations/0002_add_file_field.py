from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),  # или последняя существующая миграция (посмотрите номер)
    ]
    operations = [
        migrations.AddField(
            model_name='section',
            name='file',
            field=models.FileField(
                upload_to='section_files/',
                blank=True,
                null=True,
                verbose_name='Файл для скачивания'
            ),
        ),
    ]