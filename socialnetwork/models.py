from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
import os


def validate_email(email):
    if not settings.HUNTER.ismailvalid(email):
        raise ValidationError('E-mail is not valid')


class UserProfile(models.Model):
    """
    This model enriches standard Django User model with data and uses it for authentication purposes
    """

    class Meta:
        verbose_name = 'User Profile'

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255, verbose_name='Name', default='', blank=True,
                            help_text='First Name')
    surname = models.CharField(max_length=255, verbose_name='Surname', default='', blank=True,
                               help_text='Last Name')
    email = models.EmailField(verbose_name='E-mail', validators=[validate_email], blank=False,
                              help_text='Required. Personal e-mail address')
    site = models.URLField(verbose_name='Web-site', default='', blank=True,
                           help_text='Personal Web-page')
    country = models.CharField(max_length=255, verbose_name='Country', blank=True)
    city = models.CharField(max_length=255, verbose_name='City', default='', blank=True)
    employment = models.CharField(max_length=255, verbose_name='Employment', default='', blank=True,
                                  help_text='Place of work')
    avatar = models.FileField(verbose_name='Avatar picture', storage=os.path.join(settings.BASE_DIR, 'data'),
                              blank=True)

    @property
    def location(self):
        return ', '.join(filter(None, [self.country.capitalize(), self.city.capitalize()]))

    @property
    def likes_count(self):
        return sum([post.likes for post in Post.objects.filter(user=self.user)])

    @property
    def posts_count(self):
        return Post.objects.filter(user=self.user).count()

    def save(self, *args, **kwargs):

        validate_email(self.email)
        person = settings.CLEAR_BIT.PersonData(self.email)

        self.name = self.name or person.name
        self.surname = self.surname or person.surname
        self.country = self.country or person.country
        self.city = self.city or person.city
        self.site = self.site or person.site
        self.employment = self.employment or person.employment

        # Create User authentication and update some fields
        if not self.user.pk:
            self.user = User.objects.create_user(username=self.user.username, password=self.user.password)
        self.user.first_name = self.name
        self.user.last_name = self.surname
        self.user.email = self.email
        self.user.is_staff = False

        self.user.save()  # mandatory as create_user is not recognized as save operation

        super().save(*args, **kwargs)

    def __str__(self):
        if self.name or self.surname:
            return f'{self.name.capitalize()} {self.surname.capitalize()} ({self.user.username})'
        else:
            return self.user.username


class Post(models.Model):
    """
    Model responsible for storing one post with its likes and references to the creator and 'likers'
    """
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE,
                             help_text='User submitted a post', default='')
    content = models.TextField(verbose_name='Post content', default='')
    timestamp = models.DateTimeField(verbose_name='Created', auto_now_add=True,
                                     help_text='Post creation time')

    @property
    def likes(self):
        return Like.objects.filter(post=self).count()

    @property
    def user_profile(self):
        return UserProfile.objects.get(user=self.user)

    @property
    def text_likes(self):
        return f'Like{"s" if str(self.likes)[-1] != "1" else ""}'

    def __str__(self):
        return f'{str(self.user)}: {" ".join(self.content.split()[:20])}'


class Like(models.Model):
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)


class ResponseStatus(models.Model):
    """
    Model for serializing HTTP responses
    """

    class Meta:
        managed = False

    status = models.TextField(verbose_name='Status', default='',
                              choices=(('fail', 'Fail'), ('success', 'Success')))
    message = models.TextField(verbose_name='Message', default='')
