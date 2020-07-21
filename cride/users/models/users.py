from django.db import models
from django.contrib.auth.models import AbstractUser
from cride.utils.models import CRideModel
from django.core.validators import RegexValidator


class User(CRideModel, AbstractUser):

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that emal already exists.'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must contain from 9 to 15 digits.'
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_client = models.BooleanField(
        'client status',
        default=True,
        help_text='Clients are the main type of users'
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user have verified its email address.'
    )

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username
