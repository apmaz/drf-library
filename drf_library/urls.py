"""
URL configuration for drf_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/library/book/", include("book.urls", namespace="book")),
    path("api/v1/library/borrow/", include("borrow.urls", namespace="borrow")),
    path("api/v1/library/payment/", include("payments.urls", namespace="payment")),
    path("api/v1/library/user/", include("user.urls", namespace="user")),
    path("__debug__/", include("debug_toolbar.urls")),
]
