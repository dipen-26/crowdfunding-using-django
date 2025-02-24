from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .models import Contribution
from decimal import Decimal




from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .forms import RegisterForm, UserRegisterForm
from .models import Campaign
import logging

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('campaigns')
    else:
        form = UserRegisterForm()
    return render(request, 'auth_templates/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('campaigns')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'auth_templates/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
        'joined_date': user.date_joined.strftime('%B %Y')
    }
    return render(request, 'auth_templates/profile.html', context)

def home(request):
    campaigns = Campaign.objects.all()
    context = {'campaigns': campaigns}
    return render(request, 'index.html', context)

@login_required
def register_campaign(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.owner = request.user
            campaign.save()
            messages.success(request, "Campaign registered successfully!")
            return redirect('campaigns')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'campaign_register.html', {'form': form})

def campaigns(request):
    all_campaigns = Campaign.objects.all()
    return render(request, 'index.html', {'campaigns': all_campaigns})



@login_required
def contribute(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', 0))
        if amount > 0:
            Contribution.objects.create(
                campaign=campaign,
                user=request.user,
                amount=amount
            )
            campaign.amount += amount
            campaign.save()
            messages.success(request, f"Thank you for your contribution of ₹{amount}!")
            return redirect('campaign_details', campaign_id=campaign_id)
        else:
            messages.error(request, "Please enter a valid contribution amount.")
    return redirect('campaign_details', campaign_id=campaign_id)

def campaign_details(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    contributions = campaign.contributions.all().order_by('-created_at')
    return render(request, 'campaign_details.html', {
        'campaign': campaign,
        'contributions': contributions
    })


def faqs(request):
    return render(request, 'faqs.html')
