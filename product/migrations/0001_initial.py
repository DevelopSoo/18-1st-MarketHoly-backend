# Generated by Django 3.1.7 on 2021-03-18 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=60)),
                ('price', models.IntegerField()),
                ('image_url', models.CharField(max_length=3000)),
                ('sales_unit', models.CharField(max_length=30, null=True)),
                ('amount', models.CharField(max_length=30, null=True)),
                ('origin', models.CharField(max_length=30, null=True)),
                ('expiration_date', models.CharField(max_length=100, null=True)),
                ('stock', models.IntegerField()),
                ('content', models.TextField()),
                ('uploaded_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='StorageMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8)),
            ],
            options={
                'db_table': 'storage_methods',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
            options={
                'db_table': 'sub_categories',
            },
        ),
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_product', to='product.product')),
                ('to_product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_product', to='product.product')),
            ],
            options={
                'db_table': 'product_options',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_options',
            field=models.ManyToManyField(related_name='options', through='product.ProductOption', to='product.Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='storage_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.storagemethod'),
        ),
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.subcategory'),
        ),
        migrations.CreateModel(
            name='DiscountRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_rate', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'db_table': 'discount_rate',
            },
        ),
        migrations.CreateModel(
            name='DailySpecialDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_discount_rate', models.IntegerField()),
                ('start_date', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'db_table': 'daily_special_discount',
            },
        ),
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('product_allergy', models.ManyToManyField(to='product.Product')),
            ],
            options={
                'db_table': 'allergies',
            },
        ),
    ]
