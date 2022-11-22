from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken

from accounts.models import User
from studios.models import Card, Payment, Subscription, ClassBooking
from .serializers import RegisterSerializer, UserProfileSerializer, UserCardSerializer
from studios.serializers import PaymentsSerializer, SubscriptionSubscribeSerializer, ClassBookingUserSerializer

# register user
class RegisterUserAPIView(CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

# view user
class UserProfileView(RetrieveAPIView):
  serializer_class = UserProfileSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    if (self.request.user.id == self.kwargs['user_id']):
      return get_object_or_404(User, id=self.kwargs['user_id'])
    else:
      raise InvalidToken("This action is not authorized for this user.")

# user can edit their profile
class UserProfileEditView(UpdateAPIView):
  serializer_class = UserProfileSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    if (self.request.user.id == self.kwargs['user_id']):
      return self.request.user
    else:
      raise InvalidToken("This action is not authorized for this user.")

# user can create a card
class UserCardCreateView(CreateAPIView):
  serializer_class = UserCardSerializer
  permission_classes = [IsAuthenticated]

# user can update their card info
class UserCardUpdateView(UpdateAPIView):
  serializer_class = UserCardSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    current_user = User.objects.filter(id=self.request.user.id)[0]
    return get_object_or_404(Card, user=current_user)

# user can see their payments history
class UserPaymentHistoryView(ListAPIView):
  serializer_class = PaymentsSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    current_user = User.objects.filter(id=self.request.user.id)[0]
    return Payment.objects.filter(user=current_user)

# user can see future upcoming payment
class UserFuturePaymentView(RetrieveAPIView):
  serializer_class = SubscriptionSubscribeSerializer
  permission_classes = [IsAuthenticated]
  
  def get_object(self):
    current_user = User.objects.filter(id=self.request.user.id)[0]
    return get_object_or_404(Subscription, user=current_user)

# user can update their subscription
class UserUpdateSubscriptionView(UpdateAPIView):
  serializer_class = SubscriptionSubscribeSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    current_user = User.objects.filter(id=self.request.user.id)[0]
    return get_object_or_404(Subscription, user=current_user)

# user can see their class bookings
class UserClassBookingsView(ListAPIView):
  serializer_class = ClassBookingUserSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    current_user = User.objects.filter(id=self.request.user.id)[0]
    return ClassBooking.objects.filter(user=current_user).order_by('studio_class__start_date')



  
