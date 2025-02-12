import logging
from django.shortcuts import render, redirect, get_object_or_404
logger = logging.getLogger(__name__)
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, CampaignForm
from .models import Campaign, CampaignImage

def register(request):
    logger.info("CSRF Token: %s", request.META.get('CSRF_COOKIE'))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'auth_templates/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'auth_templates/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'auth_templates/profile.html')

def home(request):
    return render(request, 'index.html')

@login_required
def register_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')  # Get multiple images

        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.owner = request.user
            campaign.save()

            for file in files[:5]:  # Save up to 5 images
                CampaignImage.objects.create(campaign=campaign, image=file)

            messages.success(request, "Campaign registered successfully!")
            return redirect('campaigns')
    else:
        form = CampaignForm()
    return render(request, 'campaign_register.html', {'form': form})

def campaigns(request):
    all_campaigns = Campaign.objects.all()
    return render(request, 'campaigns.html', {'campaigns': all_campaigns})

def campaign_details(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    images = campaign.images.all()
    return render(request, 'campaign_details.html', {'campaign': campaign, 'images': images})

def faqs(request):
    return render(request, 'faqs.html')

def about(request):
    return render(request, 'about.html')
