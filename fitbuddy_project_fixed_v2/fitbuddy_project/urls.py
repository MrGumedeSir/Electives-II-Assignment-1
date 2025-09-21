from django.urls import path
from . import views
app_name = 'fitbuddy'
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activity/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('book/<int:session_id>/', views.book_session, name='book_session'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('log/water/', views.log_water, name='log_water'),
    path('log/activity/', views.log_activity, name='log_activity'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
]
from django.urls import path
from . import views 