# Generated by Django 4.2.13 on 2024-05-10 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ratingAuthor", models.SmallIntegerField(default=0)),
                (
                    "authorUser",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "categoryName",
                    models.CharField(
                        choices=[
                            ("SP", "Спорт"),
                            ("PO", "Политика"),
                            ("CU", "Культура"),
                            ("ED", "Образование"),
                            ("HE", "Здравоохранение"),
                            ("CR", "Криминал"),
                            ("EC", "Экономика"),
                            ("OT", "Другие"),
                        ],
                        default="OTHER",
                        max_length=2,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "postType",
                    models.CharField(
                        choices=[("NE", "Новость"), ("AR", "Статья")],
                        default="ARTICLE",
                        max_length=2,
                    ),
                ),
                ("autoDate", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=128)),
                ("postText", models.TextField()),
                ("postRating", models.SmallIntegerField(default=0)),
                (
                    "postAuthor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="news_project.author",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PostCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "categoryConnection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="news_project.category",
                    ),
                ),
                (
                    "postConnection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="news_project.post",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="postCategory",
            field=models.ManyToManyField(
                through="news_project.PostCategory", to="news_project.category"
            ),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("commentText", models.TextField()),
                ("commentDate", models.DateTimeField(auto_now_add=True)),
                ("commentRating", models.SmallIntegerField(default=0)),
                (
                    "commentPost",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="news_project.post",
                    ),
                ),
                (
                    "commentUser",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
