from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView
from .models import Product, SwapedUser, Purchase, Category
from .forms import RegistForm, AddProductForm, PurchaseForm, SearchForm, ShippedForm, DeliveredForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.db import models
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login


class MainView(ListView):
    model = Product
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        return context 

    def get_queryset(self):
        qset = super().get_queryset()
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        if category == 'women':
            qset = qset.filter(category__parent__name='Women')
        elif category == 'men':
            qset = qset.filter(category__parent__name='Men')
        if search:
            qset = qset.filter(
                Q(name__icontains=search)|
                Q(brand__icontains=search)|
                Q(description__icontains=search)
            )
        if self.request.user.is_authenticated:
            qset = qset.exclude(seller=self.request.user)
        return qset.filter(is_active=True)
    
class RegistView(FormView):
    model = SwapedUser
    form_class = RegistForm
    template_name = "registration.html"
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object, backend="django.contrib.auth.backends.ModelBackend")
        return redirect(self.get_success_url())
    
class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "addproduct.html"
    form_class = AddProductForm
    success_url = reverse_lazy("main")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent__isnull=True)
        context['subcategories'] = Category.objects.filter(parent__isnull=False)
        return context

    def form_valid(self, form):
        print("USER:", self.request.user, type(self.request.user))
        product = form.save(commit=False)
        product.seller = self.request.user
        product.save()
        messages.success(self.request, "The item has been successfully added! You can track its status in the Profile tab.")
        return super().form_valid(form)

class CartView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "cart.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('pk')
        context['product'] = get_object_or_404(Product, pk=product_id)
        return context
        
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['products'] = Product.objects.filter(seller = self.request.user)
        context['purchases'] = Purchase.objects.filter(buyer=self.request.user)
        return context

class CheckoutView(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = "checkout.html"
    form_class = PurchaseForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        purchase = form.save(commit=False)
        product_id = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_id)
        purchase.product = product
        purchase.seller = product.seller
        purchase.buyer = self.request.user
        purchase.total_price = product.price
        purchase.purchase_transaction()
        purchase.save()
        messages.success(self.request, "Payment has been successfully completed! You can track status of your order in the Profile tab.")
        return super().form_valid(form)

class ShippedView(LoginRequiredMixin, UpdateView):
    model = Purchase
    form_class = ShippedForm
    template_name = "confirm_shipment_delivery.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        purchase = self.get_object()
        if purchase.seller == self.request.user and form.cleaned_data['confirm']:
            purchase.shipped()
            return redirect(self.success_url)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase = self.get_object()
        context['purchase'] = purchase
        context['product'] = purchase.product
        context['user'] = self.request.user
        return context

class DeliveredView(LoginRequiredMixin, UpdateView):
    model = Purchase
    form_class = DeliveredForm
    template_name = "confirm_shipment_delivery.html"
    success_url = reverse_lazy("profile")
    
    def form_valid(self, form):
        purchase = self.get_object()
        if purchase.buyer == self.request.user and form.cleaned_data['confirm']:
            purchase.confirm_delivery()
            return redirect(self.success_url)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase = self.get_object()
        context['purchase'] = purchase
        context['product'] = purchase.product
        context['user'] = self.request.user
        return context
