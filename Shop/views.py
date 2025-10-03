from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView
from .models import Product, SwapedUser
from .forms import RegistForm, AddProductForm
from django.urls import reverse_lazy
from django.shortcuts import redirect


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
    
class AddProductView(CreateView):
    model = Product
    fields = ["name", "product_type", "size", "brand", "price", "description"]
    template_name = "addproduct.html"
    form_class = AddProductForm
    success_url = reverse_lazy("main")
