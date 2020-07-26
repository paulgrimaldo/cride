from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import jwt

from celery.decorators import task, periodic_task

from cride.users.models import User
from cride.rides.models import Ride


@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)
    subject = 'Welcome @{}! Verify your account to start using Comparte Ride'.format(user.username)
    from_email = 'Comparte Ride <noreply@comparteride.com>'
    content = render_to_string(
        'emails/users/account_verification.html',
        {'token': verification_token, 'user': user}
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()


def gen_verification_token(user):
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode()


@periodic_task(name='disable_finished_rides', run_every=timedelta(hours=1))
def disable_finished_rides():
    now = timezone.now()
    offset = now + timedelta(hours=1)
    rides = Ride.objects.filter(arrival_date__gte=now, arrival_date__lte=offset, is_active=True)
    rides.update(is_active=False)
