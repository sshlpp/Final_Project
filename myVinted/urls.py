from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from Shop.views import MainView, RegistView, AddProductView, CartView, ProfileView, CheckoutView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name="main"),
    path('registration/', RegistView.as_view(), name="registration"),
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(next_page='/'), name="logout"),
    path('addproduct/', AddProductView.as_view(), name="add"),
    path('add_to_cart/<int:pk>/', CartView.as_view(), name="cart"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('checkout/<int:pk>/', CheckoutView.as_view(), name="checkout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
