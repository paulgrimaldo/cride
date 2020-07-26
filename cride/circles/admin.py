from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from cride.circles.models import Circle
from cride.rides.models import Ride
import csv


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display = ('slug_name', 'name', 'is_public', 'verified', 'is_limited', 'members_limit')
    search_fields = ('slug_name', 'name')
    list_filter = ('is_public', 'verified', 'is_limited')

    actions = ['make_verified', 'make_unverified', 'download_todays_rides']

    def make_verified(self, request, queryset):
        queryset.update(verified=True)

    make_verified.short_description = 'Make selected circles verified'

    def make_unverified(self, request, queryset):
        queryset.update(verified=False)

    make_unverified.short_description = 'Make selected circles unverified'

    def download_todays_rides(self, request, queryset):
        now = timezone.now()
        start = datetime(now.year, now.month, now.day, 0, 0, 0)
        end = start + timedelta(days=1)
        rides = Ride.objects.filter(
            offered_in__in=queryset.values_list('id'),
            departure_date__gte=start,
            departure_date__lte=end
        )
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=rides.csv'
        writer = csv.writer(response)
        writer.writerow([
            'id',
            'passengers',
            'departure_location',
            'departure_date',
            'arrival_location',
            'arrival_date',
            'rating'
        ])
        for ride in rides:
            writer.writerow([
                str(ride.pk),
                str(ride.passengers.count()),
                str(ride.departure_location),
                str(ride.departure_date),
                str(ride.arrival_location),
                str(ride.arrival_date),
                str(ride.rating)
            ])
        return response

    download_todays_rides.short_description = 'Download todays rides'
