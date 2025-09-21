from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Activity, Session, Booking, HydrationLog, ActivityLog, User
from .forms import RegisterForm, HydrationForm, ActivityLogForm

def home(request):
    activities = Activity.objects.prefetch_related('sessions').all()
    return render(request, 'fitbuddy/home.html', {'activities': activities})

@login_required
def dashboard(request):
    user = request.user
    now = timezone.now()
    bookings = user.bookings.select_related('session__activity').all()
    hydration_today = user.hydration_logs.filter(created_at__date=now.date())
    activity_logs = user.activity_logs.order_by('-created_at')[:10]
    return render(request, 'fitbuddy/dashboard.html', {
        'bookings': bookings,
        'hydration_today': hydration_today,
        'activity_logs': activity_logs
    })

def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    sessions = activity.sessions.all().order_by('start_time')
    return render(request, 'fitbuddy/activity_detail.html', {'activity': activity, 'sessions': sessions})

@login_required
def book_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    # rudimentary capacity check
    if session.bookings.filter(status='confirmed').count() >= session.capacity:
        messages.error(request, "Session is full.")
        return redirect('fitbuddy:activity_detail', pk=session.activity.pk)
    booking, created = Booking.objects.get_or_create(user=request.user, session=session)
    booking.status = 'confirmed'
    booking.save()
    messages.success(request, "Booking confirmed.")
    return redirect('fitbuddy:dashboard')

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, "Booking cancelled.")
    return redirect('fitbuddy:dashboard')

@login_required
def log_water(request):
    if request.method == 'POST':
        form = HydrationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount_ml']
            HydrationLog.objects.create(user=request.user, amount_ml=amount)
            messages.success(request, "Water logged.")
            return redirect('fitbuddy:dashboard')
    return redirect('fitbuddy:dashboard')

@login_required
def log_activity(request):
    if request.method == 'POST':
        form = ActivityLogForm(request.POST)
        if form.is_valid():
            ActivityLog.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                duration_minutes=form.cleaned_data['duration_minutes']
            )
            messages.success(request, "Activity logged.")
            return redirect('fitbuddy:dashboard')
    return redirect('fitbuddy:dashboard')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('fitbuddy:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'fitbuddy/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('fitbuddy:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'fitbuddy/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('fitbuddy:home')