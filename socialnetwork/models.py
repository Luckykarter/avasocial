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

    def save(self, *args, **kwargs):

        validate_email(self.email)
        person = settings.CLEAR_BIT.PersonData(self.email)

        self.name = person.name if not self.name else self.name
        self.surname = person.surname if not self.surname else self.surname
        self.country = person.country if not self.country else self.country
        self.city = person.city if not self.city else self.city
        self.site = person.site if not self.site else self.site
        self.employment = person.employment if not self.employment else self.employment

        # Create User authentication and update some fields
        self.user = User.objects.create_user(self.user.username, password=self.user.password)
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
    timestamp = models.DateTimeField(verbose_name='Created', auto_now=True,
                                     help_text='Post creation time')
    likes = models.IntegerField(default=0)

    likes_users = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{str(self.user)}: {" ".join(self.content.split()[:20])}'


class ResponseStatus(models.Model):
    """
    Model for serializing HTTP responses
    """

    class Meta:
        managed = False

    status = models.TextField(verbose_name='Status', default='',
                              choices=(('fail', 'Fail'), ('success', 'Success')))
    message = models.TextField(verbose_name='Message', default='')
