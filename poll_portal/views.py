# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden
from functools import wraps
from .models import Poll, Vote
from .forms import CreatePollForm, RegisterForm


def is_admin(user):
    return user.is_staff or user.is_superuser


def admin_required(view_func):
    """Redirect anonymous users to login, redirect non-admin users to home."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.conf import settings
            from django.utils.http import urlencode
            login_url = getattr(settings, 'LOGIN_URL', 'login')
            params = urlencode({'next': request.get_full_path()})
            return redirect(f'/{login_url}/?{params}' if login_url.startswith('/') else f'/login/?{params}')
        if not is_admin(request.user):
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped


# ─── Authentication ───────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'poll_portal/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'poll_portal/login.html', {'next': request.GET.get('next', '')})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─── Public / Voter Views ─────────────────────────────────────────────────────

def home(request):
    polls = Poll.objects.filter(is_active=True)
    voted_polls = []
    if request.user.is_authenticated:
        voted_polls = list(Vote.objects.filter(user=request.user).values_list('poll_id', flat=True))
    return render(request, 'poll_portal/home.html', {
        'polls': polls,
        'voted_polls': voted_polls,
    })


@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id, is_active=True)

    # Check if user already voted
    if Vote.objects.filter(user=request.user, poll=poll).exists():
        messages.warning(request, 'You have already voted in this poll.')
        return redirect('home')

    if request.method == 'POST':
        selected_option = request.POST.get('poll')
        if selected_option == 'option1':
            poll.option_one_count += 1
            choice_label = poll.option_one
        elif selected_option == 'option2':
            poll.option_two_count += 1
            choice_label = poll.option_two
        elif selected_option == 'option3':
            poll.option_three_count += 1
            choice_label = poll.option_three
        else:
            messages.error(request, 'Please select an option before submitting.')
            return render(request, 'poll_portal/vote.html', {'poll': poll})

        poll.save()
        Vote.objects.create(user=request.user, poll=poll, choice=selected_option)
        messages.success(request, f'Your vote for "{choice_label}" has been recorded!')
        return redirect('home')

    return render(request, 'poll_portal/vote.html', {'poll': poll})


def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    # Non-admins can only see results if published
    if not (request.user.is_authenticated and is_admin(request.user)):
        if not poll.result_published:
            messages.error(request, 'Results for this poll have not been published yet.')
            return redirect('home')
    user_vote = None
    if request.user.is_authenticated:
        vote_obj = Vote.objects.filter(user=request.user, poll=poll).first()
        if vote_obj:
            user_vote = vote_obj.choice
    return render(request, 'poll_portal/results.html', {
        'poll': poll,
        'user_vote': user_vote,
    })


# ─── Admin-Only Views ─────────────────────────────────────────────────────────

@admin_required
def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.created_by = request.user
            poll.save()
            messages.success(request, 'Poll created successfully!')
            return redirect('home')
    else:
        form = CreatePollForm()
    return render(request, 'poll_portal/create.html', {'form': form})


@admin_required
def delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':
        poll.delete()
        messages.success(request, 'Poll deleted successfully.')
        return redirect('home')
    return render(request, 'poll_portal/delete.html', {'poll': poll})


@admin_required
def declare_result(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.result_published = not poll.result_published
    poll.save()
    status = 'published' if poll.result_published else 'hidden'
    messages.success(request, f'Results have been {status}.')
    return redirect('admin_dashboard')


@admin_required
def toggle_active(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.is_active = not poll.is_active
    poll.save()
    status = 'activated' if poll.is_active else 'closed'
    messages.success(request, f'Poll has been {status}.')
    return redirect('admin_dashboard')


@admin_required
def admin_dashboard(request):
    polls = Poll.objects.all()
    total_votes = Vote.objects.count()
    total_polls = polls.count()
    active_polls = polls.filter(is_active=True).count()
    return render(request, 'poll_portal/admin_dashboard.html', {
        'polls': polls,
        'total_votes': total_votes,
        'total_polls': total_polls,
        'active_polls': active_polls,
    })


@admin_required
def voters_list(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    votes = Vote.objects.filter(poll=poll).select_related('user').order_by('-voted_on')
    return render(request, 'poll_portal/voters.html', {
        'poll': poll,
        'votes': votes,
    })
