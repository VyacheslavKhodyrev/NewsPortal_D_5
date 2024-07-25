from django.core.management.base import BaseCommand, CommandError
from news_project.models import Post, Category


class Command(BaseCommand):
    help = "command to delete posts by category"

    def add_arguments(self, parser):
        parser.add_argument('categoryName', type=str)

    def handle(self, *args, **options):
        answer = input(f'Do you really want to delete all articles {options["categoryName"]}? yes/no ')
        if answer != 'yes':
            self.stdout.write(self.style.ERROR("отменено"))
            return
        try:
            category = Category.objects.get(categoryName = options['categoryName'])
            Post.objects.filter(postCategory = category).delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted all news from category {category.categoryName}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category'))

