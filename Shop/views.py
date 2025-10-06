from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView
from .models import Product, SwapedUser, Purchase
from .forms import RegistForm, AddProductForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView

class MainView(ListView):
    model = Product
    template_name = "main.html"

class RegistView(FormView):
    model = SwapedUser
    form_class = RegistForm
    template_name = "registration.html"
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        self.object = form.save()
        # login(self.request, self.object, backend="django.contrib.auth.backends.ModelBackend")
        return redirect(self.get_success_url())
    
class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "addproduct.html"
    form_class = AddProductForm
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        print("USER:", self.request.user, type(self.request.user))
        product = form.save(commit=False)
        product.seller = self.request.user
        product.save()
        return super().form_valid(form)

class CartView(LoginRequiredMixin, DetailView ):
    model = Product
    template_name = "cart.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('pk')
        context['product'] = get_object_or_404(Product, pk=product_id)
        return context
        
