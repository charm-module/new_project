# Generated by Django 3.2.13 on 2022-06-06 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_orderplaced_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderplaced',
            name='status',
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('PACKED', 'PACKED'), ('DELIVERED', 'DELIVERED'), ('CANCEL', 'CANCEL')], default='pending', max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.orderplaced')),
            ],
        ),
    ]
