from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(post_rating=Sum('postRating'))
        pR = 0
        pR += postRat.get('post_rating')
        commRat = self.authorUser.comment_set.aggregate(comment_rating=Sum('commentRating'))
        cR = 0
        cR += commRat.get('comment_rating')
        self.ratingAuthor = pR * 3 + cR
        self.save()


    def __str__(self):
        return self.authorUser.username



class Category(models.Model):
    SPORT = 'SP'
    POLICY = 'PO'
    CULTURE = 'CU'
    EDUCATION = 'ED'
    HEALTHCARE = 'HE'
    CRIMINAL = 'CR'
    ECONOMY = 'EC'
    OTHER = 'OT'

    CATEGORY_TOPIC = [
        (SPORT, 'Спорт'),
        (POLICY, 'Политика'),
        (CULTURE, 'Культура'),
        (EDUCATION, 'Образование'),
        (HEALTHCARE, 'Здравоохранение'),
        (CRIMINAL, 'Криминал'),
        (ECONOMY, 'Экономика'),
        (OTHER, 'Другие')
    ]

    categoryName = models.CharField(max_length=2, choices=CATEGORY_TOPIC, default='OTHER', unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.get_categoryName_display()


class Post(models.Model):
    NEWS = 'NE'
    ARTICLE = 'AR'

    CHOICE_TYPE = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]

    postType = models.CharField(max_length=2, choices=CHOICE_TYPE, default='ARTICLE')
    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    autoDate = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    postText = models.TextField()
    postRating = models.SmallIntegerField(default=0)

    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()

    def preview(self):
        return self.postText[0:20] + "..."

    def __str__(self):
        return f'{self.title}: {self.postText[:20]}', self.get_postType_display()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    postConnection = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryConnection = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    commentDate = models.DateTimeField(auto_now_add=True)
    commentRating = models.SmallIntegerField(default=0)

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()
