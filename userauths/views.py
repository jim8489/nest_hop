from django.shortcuts import get_object_or_404, render, redirect
from userauths.forms import UserRegisterForm
from django.contrib import messages
from userauths.models import User
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site  # Add this import
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False 
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))  
            
            # Build email verification link
            current_site = get_current_site(request)
            verification_url = f"http://{current_site.domain}/activate/{uid}/{token}/"
            
            # Send the email
            subject = "Activate your account"
            message = render_to_string('userauths/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            email = form.cleaned_data.get('email')
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            
            # Notify the user and return
            messages.success(request, f"Hey {user}, please confirm your email to activate your account!")
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserRegisterForm()
    
    return render(request, 'userauths/signup.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode the user ID
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Activate the user's account
        user.save()
        messages.success(request, 'Your account has been activated successfully. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        return redirect('register')
    
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from userauths.models import User

AUTH_USER_MODEL = "userauths.User"

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("The email address you entered is not registered.")
        return email

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:  
                login(request, user)
                messages.success(request, f"{user.username}, you are logged in.")
                return redirect('index')
            else:
                messages.warning(request, "Your account is not activated. Please check your email.")
        else:
            messages.warning(request, "Invalid credentials. Please try again.")
    
    return render(request, "userauths/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')  # Redirect to login page after logout
