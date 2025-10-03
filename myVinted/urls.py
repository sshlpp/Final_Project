from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from Shop.views import MainView, RegistView, AddProductView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', MainView.as_view(), name="main"),
    path('registration/', RegistView.as_view(), name="registration"),
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('addproduct/', AddProductView.as_view(), name="add"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
