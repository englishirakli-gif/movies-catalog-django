from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True)),
                ('release_year', models.PositiveIntegerField()),
                ('duration_minutes', models.PositiveIntegerField()),
                ('age_rating', models.CharField(choices=[('G', 'ყველასთვის'), ('PG', 'მშობლის თანხლებით'), ('PG13', '13+'), ('R', '18+')], default='G', max_length=4)),
                ('budget', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'ფილმი',
                'verbose_name_plural': 'ფილმები',
                'ordering': ['-release_year'],
            },
        ),
    ]
