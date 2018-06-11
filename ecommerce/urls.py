"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import register_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/user/', include('accounts.api.urls', namespace='users-api')),
    url(r'^api/retail/', include('retail.api.urls', namespace='retail-api')),
    url(r'^api/order/', include('order.api.urls', namespace='order-api')),        
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        register_view, name='activate'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)