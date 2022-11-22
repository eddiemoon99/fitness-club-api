from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import CASCADE

import math
from django.db.backends.signals import connection_created
from django.dispatch import receiver
from django.db.models.expressions import RawSQL

from accounts.models import User

# sqlite doesn't natively support math functions, adding them
@receiver(connection_created)
def extend_sqlite(connection=None, **kwargs):
    if connection.vendor == "sqlite":
        cf = connection.connection.create_function
        cf('acos', 1, math.acos)
        cf('cos', 1, math.cos)
        cf('radians', 1, math.radians)
        cf('sin', 1, math.sin)
        cf('least', 2, min)
        cf('greatest', 2, max)


class Image(models.Model):
  image = models.ImageField(upload_to='studios/', null=True, blank=True)
  studio = models.ForeignKey('Studio', on_delete=models.DO_NOTHING, related_name='images')

  def __str__(self):
    return self.image.url

class Point(models.Model):
  latitude = models.FloatField()
  longitude = models.FloatField()
  studio = models.OneToOneField('Studio', on_delete=models.CASCADE, related_name='point', unique=True)
  
  def __str__(self):
    return f"{self.latitude},{self.longitude}"

  # sort points by their lat | long, based on closest to argument lat | long
  def get_points_nearby_coords(latitude, longitude, max_distance=None):
    """
    Return objects sorted by distance to specified coordinates
    which distance is less than max_distance given in kilometers
    """
    # Great circle distance formula
    gcd_formula = "6371 * acos(least(greatest(\
    cos(radians(%s)) * cos(radians(latitude)) \
    * cos(radians(longitude) - radians(%s)) + \
    sin(radians(%s)) * sin(radians(latitude)) \
    , -1), 1))"
    distance_raw_sql = RawSQL(
        gcd_formula,
        (latitude, longitude, latitude)
    )
    qs = Point.objects.all() \
    .annotate(distance=distance_raw_sql) \
    .order_by('distance')
    if max_distance is not None:
        qs = qs.filter(distance__lt=max_distance)
    return qs

class Amenity(models.Model):
  type = models.CharField(max_length=200)
  quantity = models.IntegerField()
  studio = models.ForeignKey('Studio', on_delete=models.DO_NOTHING, related_name='amenities')

  def __str__(self):
    return f"{self.type} / {self.quantity}"

class Keyword(models.Model):
  keyword = models.CharField(max_length=200)
  studio_class = models.ForeignKey('StudioClass', on_delete=models.DO_NOTHING, related_name='keywords')

  def __str__(self):
    return self.keyword

STATUS_CHOICES = (('active', 'active'), ('cancelled', 'cancelled'))
class StudioClass(models.Model):
  name = models.CharField(max_length=200)
  description = models.CharField(max_length=200)
  coach = models.CharField(max_length=200)
  capacity = models.PositiveIntegerField()
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  recurrence_end = models.DateTimeField()
  studio = models.ForeignKey('Studio', on_delete=models.DO_NOTHING, related_name='classes')
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

  def __str__(self):
    return self.name

  class Meta:
    ordering = ['start_time']


class Studio(models.Model):
  name = models.CharField(max_length=200)
  address = models.CharField(max_length=200)
  postal_code = models.CharField(max_length=200)
  phone_number = models.CharField(max_length=200)

  def __str__(self):
    return self.name

class SubscriptionPlan(models.Model):
  price = models.FloatField()
  duration = models.PositiveIntegerField()

  def __str__(self):
    return f"{self.price}-{self.duration}days"

class Subscription(models.Model):
  start_date = models.DateField()
  next_date = models.DateField()
  user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='subscription')
  price = models.FloatField()
  duration = models.PositiveIntegerField()
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

  def __str__(self):
    return f"{self.user.username} - subscription"

class Card(models.Model):
  user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='card')
  last_name = models.CharField(max_length=200)
  first_name = models.CharField(max_length=200)
  address = models.CharField(max_length=200)
  phone_number = models.CharField(max_length=200)
  card_number = models.BigIntegerField()
  card_expiry = models.DateField()
  card_cvv = models.IntegerField()

  def __str__(self):
    return f"{self.user.username} - card information"

class Payment(models.Model):
  date = models.DateTimeField()
  amount = models.FloatField()
  card = models.ForeignKey(Card, on_delete=models.DO_NOTHING, related_name='payments')
  user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='payments')

  def __str__(self):
    return f"{self.user.username} - payment ({self.date})"

class ClassBooking(models.Model):
  studio_class = models.ForeignKey(StudioClass, on_delete=models.DO_NOTHING, related_name='bookings')
  user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='bookings')

  def __str__(self):
    return f"{self.studio_class.name} - {self.user.username} ({self.id})"