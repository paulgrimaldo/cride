from django.db import models

from cride.utils.models import CRideModel


class Circle(CRideModel):
    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)
    about = models.CharField('circle description', max_length=255)
    picture = models.ImageField(upload_to='circles/pictures', blank=True, null=True)

    members = models.ManyToManyField(
        "users.User",
        through='circles.Membership',
        through_fields=('circle', 'user')
    )

    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    verified = models.BooleanField(
        'verified circle',
        default=False,
        help_text='Verified circle are also know as official communities'
    )

    is_public = models.BooleanField(
        default=True,
        help_text='Public circles are listed in the main page'
    )
    is_limited = models.BooleanField(
        default=False,
        help_text='Limited circles can grow up to a fixed number of members'
    )
    members_limit = models.PositiveIntegerField(
        default=0,
        help_text='If circle is limited, this will be the limit on the number of members'
    )

    def __str__(self):
        return self.name

    class Meta(CRideModel.Meta):
        ordering = ['-rides_taken', '-rides_offered']
