from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='korisnik',
            name='role',
            field=models.CharField(choices=[('adm', 'admin'), ('prof', 'profesor'), ('stu', 'student')], max_length=50),
        ),
    ]
