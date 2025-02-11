from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from .forms import CustomerOrganizationForm
from .models import Asset, CustomerOrganization


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

def customer_organizations(request):
    return render(request,'customer_organization.html')


class CreateCustomerOrganization(CreateView):
    model = CustomerOrganization
    form_class = CustomerOrganizationForm
    template_name = "customer_organization.html"
    success_url = '/'

    def get_context_data(self, **kwargs):
        data = super(CreateCustomerOrganization, self).get_context_data(**kwargs)
        if self.request.POST:
            data['form'] = CustomerOrganizationForm(self.request.POST)

        else:
            data['form'] = CustomerOrganizationForm()
        return data

    def get_success_url(self):
        return reverse("/")

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        org = CustomerOrganization.objects.get(name=form.instance.name)
        org.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        if not form.is_valid():
            messages.error(self.request,
                           "You already have same object")
            return render(self.request, self.template_name,
                          {'form': form})