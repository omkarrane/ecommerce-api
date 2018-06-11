from django.conf.urls import url
from django.contrib import admin


from .views import (
    UserCreateAPIView,
    UserLoginAPIView,
    SecuredAPIView,
    CreateUserInfoAPIView,
    DisplayUserInfoAPIView,
    UpdateUserInfoAPIView,
    AddUserAddressAPIView,
    DisplayUserAddressAPIView,
    UpdateUserAddressAPIView,
    DeleteUserAddressAPIView,
)

app_name = 'accounts'


urlpatterns = [
    url(r'^login$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register$', UserCreateAPIView.as_view(), name='register'),
    url(r'^secure$', SecuredAPIView.as_view(), name='secured'),
    url(r'^create/info$', CreateUserInfoAPIView.as_view(), name='create-user-info'),
    url(r'^get/info$', DisplayUserInfoAPIView.as_view(), name='get-user-info'),
    url(r'^update/info$', UpdateUserInfoAPIView.as_view(), name='update-user-info'),
    url(r'^add/address$', AddUserAddressAPIView.as_view(), name='add-user-address'),
    url(r'^list/address$', DisplayUserAddressAPIView.as_view(), name='list-user-address'),
    url(r'^update/address/(?P<id>\d+)$', UpdateUserAddressAPIView.as_view(), name='update-user-address'),                               
    url(r'^delete/address/(?P<id>\d+)$', DeleteUserAddressAPIView.as_view(), name='delete-user-address'),                               
]
