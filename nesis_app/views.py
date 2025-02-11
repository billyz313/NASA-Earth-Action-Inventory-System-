from django.shortcuts import render, get_object_or_404, redirect
from .models import Asset


def index(request):
    return render(request, 'index.html')

def login(request):
    response = redirect('accounts/google/login/')
    return response


def inventory(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')

    assets = Asset.objects.all()

    if search_query:
        assets = assets.filter(name__icontains=search_query)
    if category_filter:
        assets = assets.filter(category=category_filter)
    if status_filter:
        assets = assets.filter(status=status_filter)

    return render(request, 'inventory.html', {'assets': assets})


def asset_detail(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    related_assets = Asset.objects.filter(category=asset.category).exclude(id=asset.id)[:3]

    return render(request, 'asset_detail.html', {'asset': asset, 'related_assets': related_assets})


def hold_route(request):
    return render(request, 'index.html')