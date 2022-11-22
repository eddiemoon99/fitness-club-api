from django.urls import path, include
from accounts import views

from .views import UserClassBookingsView, RegisterUserAPIView, UserProfileView, UserProfileEditView, UserCardCreateView, UserCardUpdateView, UserPaymentHistoryView, UserFuturePaymentView, UserUpdateSubscriptionView


app_name = 'accounts'

urlpatterns = [
  path('register/', RegisterUserAPIView.as_view(), name='register'),
  path('<int:user_id>/profile/', UserProfileView.as_view(), name='user'),
  path('<int:user_id>/profile/edit/', UserProfileEditView.as_view(), name='user-edit'),
  path('card/create/', UserCardCreateView.as_view(), name='user-card-create'),
  path('card/update/', UserCardUpdateView.as_view(), name='user-card-update'),
  path('payments-history/', UserPaymentHistoryView.as_view(), name='payments-history'),
  path('payments-future/', UserFuturePaymentView.as_view(), name='payments-future'),
  path('update-subscription/', UserUpdateSubscriptionView.as_view(), name='update-subscription'),
  path('class-bookings-list/', UserClassBookingsView.as_view(), name='class-bookings-view')
]