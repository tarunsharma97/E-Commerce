from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.forms import fields, models, widgets
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation
from .models import Customer, Order


class CustomerRegistrationForm(UserCreationForm):
    email = forms.CharField(required=True, widget=forms.EmailInput
                            (attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput
                                (attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput
                                (attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        lables = {'email': 'Email'}
        widgets = {'username': forms.TextInput(
            attrs={'class': 'form-control'})}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'A user with that email already exists.')
        return email


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput
                             (attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput
                               (attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput
                                   (attrs={'autofocus': True, 'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput
                                    (attrs={'autocomplete': 'new-password', 'class': 'form-control'}), help_text=password_validation.
                                    password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput
                                    (attrs={'autocomplete': 'new-password', 'class': 'form-control'}))


class MyPasswordResetForm(PasswordResetForm):

    email = forms.CharField(label=_("Email"), max_length=254, widget=forms.EmailInput
                                   (attrs={'autofocus': True, 'autocomplete': 'email', 'class': 'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput
                                    (attrs={'autofocus': True, 'autocomplete': 'new-password', 'class': 'form-control'}), help_text=password_validation.
                                    password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput
                                    (attrs={'autocomplete': 'new-password', 'class': 'form-control'}))


class MyUserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {'username': forms.TextInput(
            attrs={'placeholder': 'Username', 'autofocus': True, 'class': 'form-control'}), 'first_name': forms.TextInput(
            attrs={'placeholder': 'First Name', 'class': 'form-control'}), 'last_name': forms.TextInput(
            attrs={'placeholder': 'Last Name', 'class': 'form-control'}), 'email': forms.EmailInput(
            attrs={'placeholder': 'Email', 'class': 'form-control'})}


class MyProfileForm(forms.ModelForm):
    mobile_no = forms.CharField(label=_("Mobile number"), widget=forms.NumberInput
                                (attrs={'placeholder': 'Mobile No.', 'autocomplete': 'mobile_no', 'class': 'form-control'}))

    address1 = forms.CharField(label=_("Address"), widget=forms.TextInput
                               (attrs={'placeholder': '(Flat no. & Address)', 'autocomplete': 'address1', 'class': 'form-control'}))

    address2 = forms.CharField(label=_("Address 2 (optional)"), widget=forms.TextInput
                               (attrs={'placeholder': '(Landmark, Near by)', 'autocomplete': 'address2', 'class': 'form-control'}))

    city = forms.CharField(label=_("City"), widget=forms.TextInput
                           (attrs={'placeholder': 'City', 'autocomplete': 'city', 'class': 'form-control'}))

    zip_code = forms.CharField(label=_("Zip code"), widget=forms.NumberInput
                               (attrs={'placeholder': 'Pin code / Zip code', 'autocomplete': 'zip_code', 'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ['mobile_no', 'address1', 'address2',
                  'city', 'state', 'zip_code', 'profile_image']
        widgets = {'state': forms.Select(
            attrs={'class': 'form-control'})}


class MyUserCheckoutForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {'first_name': forms.TextInput(
            attrs={'placeholder': 'First Name', 'class': 'form-control'}), 'last_name': forms.TextInput(
            attrs={'placeholder': 'Last Name', 'class': 'form-control'})}


class MyCheckoutForm(forms.ModelForm):
    mobile_no = forms.CharField(label=_("Mobile number"), widget=forms.NumberInput
                                (attrs={'placeholder': 'Mobile No.', 'autocomplete': 'mobile_no', 'class': 'form-control'}))

    address1 = forms.CharField(label=_("Address"), widget=forms.TextInput
                               (attrs={'placeholder': '(Flat no. & Address)', 'autocomplete': 'address1', 'class': 'form-control'}))

    address2 = forms.CharField(label=_("Address 2 (optional)"), widget=forms.TextInput
                               (attrs={'placeholder': '(Landmark, Near by)', 'autocomplete': 'address2', 'class': 'form-control'}))

    city = forms.CharField(label=_("City"), widget=forms.TextInput
                           (attrs={'placeholder': 'City', 'autocomplete': 'city', 'class': 'form-control'}))

    zip_code = forms.CharField(label=_("Zip code"), widget=forms.NumberInput
                               (attrs={'placeholder': 'Pin code / Zip code', 'autocomplete': 'zip_code', 'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ['mobile_no', 'address1', 'address2',
                  'city', 'state', 'zip_code']
        widgets = {'state': forms.Select(
            attrs={'class': 'form-control'})}


PAYMENT_OPTION_CHOICES = (
    ('Stripe', 'Stripe'),
    ('Paypal', 'Paypal'),
    ('Cash on delivery', 'Cash on delivery'),
)


class PaymentOptionForm(forms.ModelForm):
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_OPTION_CHOICES)

    class Meta:
        model = Order
        fields = ['payment_option']
