from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Studio, Image, Point, StudioClass, Amenity, SubscriptionPlan, Subscription, Payment, Card, ClassBooking

class ImageSerializer(serializers.ModelSerializer):
  image = serializers.CharField(source='image.url', read_only=True)
  class Meta:
    model = Image
    fields = ['image']

class ClassesSerializer(serializers.ModelSerializer):
  class Meta:
    model = StudioClass
    fields = ['name']

class AmenitiesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Amenity
    fields = ['type', 'quantity']

class StudiosSerializer(serializers.ModelSerializer):
  images = ImageSerializer(many=True)
  classes = ClassesSerializer(many=True)
  amenities = AmenitiesSerializer(many=True)
  class Meta:
    model = Studio
    fields = ['name', 'images', 'postal_code', 'phone_number', 'address', 'amenities', 'classes']

class PointSerializer(serializers.ModelSerializer):
  # latitude = serializers.CharField(source='__str__', read_only=True)
  class Meta:
    model = Point
    fields = ['latitude', 'longitude']

class StudioSerializer(serializers.ModelSerializer):
  point = PointSerializer()
  class Meta:
    model = Studio
    fields = ['name', 'address', 'point', 'postal_code', 'phone_number']

class StudioClassesSerializer(serializers.ModelSerializer):
  #studio = StudioSerializer()
  class Meta:
    model = StudioClass
    fields = ['name', 'description', 'coach', 'capacity', 'start_time', 'end_time', 'studio']

class CardSerializer(serializers.ModelSerializer):
  class Meta:
    model = Card
    fields = ['user', 'last_name', 'first_name', 'address', 'phone_number', 'card_number', 'card_expiry', 'card_cvv']

class PaymentsSerializer(serializers.ModelSerializer):
  card = CardSerializer()
  class Meta:
    model = Payment
    fields = ['date', 'amount', 'card', 'user']

class SubscriptionPlansSerializer(serializers.ModelSerializer):

  class Meta:
    model = SubscriptionPlan
    fields = ['price', 'duration']

class SubscriptionSubscribeSerializer(serializers.ModelSerializer):
  user = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
  )

  class Meta:
    model = Subscription
    fields = ['start_date', 'next_date', 'user', 'price', 'duration', 'status']

  def create(self, validated_data):
    
    current_user = validated_data['user']
    has_subscription = Subscription.objects.filter(user=current_user)

    if has_subscription:
      raise PermissionDenied(detail='Already have a subscription', code=405)
    if hasattr(current_user, 'card'):
      payment = Payment(date=timezone.now(), amount=float(validated_data['price']), card=current_user.card, user=current_user)
      payment.save()
      return Subscription.objects.create(**validated_data)
    else:
      raise PermissionDenied(detail='Please add a card to your account', code=402)

class ClassSerializer(serializers.ModelSerializer):
  class Meta:
    model = StudioClass
    fields = ['name', 'description', 'coach', 'capacity', 'start_time', 'end_time', 'studio']

class ClassBookingSerializer(serializers.ModelSerializer):
  user = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
  )

  class Meta:
    model = ClassBooking
    fields = ['user']

  def create(self, validated_data):
    current_user = validated_data['user']
    class_id = self.context['request'].data['class_id']
    studio_class = StudioClass.objects.filter(id=class_id)[0]
    booking_exist = ClassBooking.objects.filter(studio_class=studio_class, user=current_user)
    if booking_exist:
      raise PermissionDenied(detail='Already booked', code=405)
    elif len(ClassBooking.objects.filter(studio_class=studio_class)) >= studio_class.capacity:
      raise PermissionDenied(detail='Class is full.', code=405)
    elif not hasattr(current_user, 'subscription') or current_user.subscription.status != 'active':
      raise PermissionDenied(detail='Need to purchase a subscription first', code=405)
    else:
      return ClassBooking.objects.create(studio_class=studio_class, user=current_user)

class ClassDroppingSerializer(serializers.ModelSerializer):
  user = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
  )

  class Meta:
    model = ClassBooking
    fields = ['user']

class ClassBookingUserSerializer(serializers.ModelSerializer):
  studio_class = ClassSerializer()
  class Meta:
    model = ClassBooking
    fields = ['studio_class', 'user']



