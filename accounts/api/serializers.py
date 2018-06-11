from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .utils import generateToken, decodeToken


import random

from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    PrimaryKeyRelatedField
)

User = get_user_model()

from accounts.models import (
    User_Info,
    User_Address,
)

class UserCreateSerializer(ModelSerializer):
    email = EmailField(label="Email Address")

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'first_name',
            'last_name'
        ]

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        return data

    def validate_email(self, value):
        data = self.get_initial()
        email = data.get("email")
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data['password']
        try:
            username = str(email.split('@')[0])
        except:
            username = str(email.split('@')[0]) + '-' + str(random.randint(100000, 992726))
        user_obj = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.is_active = False
        user_obj.save()

        current_site = 'http://127.0.0.1:8000'
        mail_subject = 'Activate your Studd account.'
        message = render_to_string('acc_activation_email.html', {
            'user': user_obj,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)).decode(),
            'token': account_activation_token.make_token(user_obj),
        })
        send_email = EmailMessage(
            mail_subject, message, to=[email]
        )
        send_email.send()
        return validated_data



class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    email = EmailField(label="Email Address", required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'token',
        ]

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        user_obj = None
        email = data.get('email', None)
        password = data["password"]
        if not email:
            raise ValidationError("An email is required")

        user = User.objects.filter(
            Q(email=email)
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials, please try again")
            token = generateToken(user_obj)
            data['token'] = token

        return data


class UserInfoSerializer(ModelSerializer):
    
    class Meta:
        model = User_Info
        fields = [
            'mobile'
        ]


class UserInfoDetailSerializer(ModelSerializer):

    class Meta:
        model = User_Info
        fields = '__all__'


class UserAddressSerializer(ModelSerializer):

    class Meta:
        model = User_Address
        fields = [
            'id',
            'city',
            'state',
            'address',
            'pincode',
        ]
        read_only_fields = [
            'id'
        ]