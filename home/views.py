from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework import viewsets
from .forms import NewUserForm, ContactForm, MessageForm
from .serializers import ContactSerializer
from .models import Contact, Message
from chat.models import ProfileAvatar


class ContactView(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


def home_response(request):
    return render(request, "home/home.html")


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Registration successful.")
            # assign a default avatar for new user
            avatar = ProfileAvatar(related_user=user)
            avatar.save()
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="home/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("user")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="home/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


def reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "home/reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': 'my-env.eba-e7eetn7u.us-east-2.elasticbeanstalk.com',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("password_reset_done")
            messages.error(request, 'This email has not been registered yet.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="home/reset.html",
                  context={"password_reset_form": password_reset_form})


@login_required()
def user_response(request):
    context={}
    user = request.user
    contacts = User.objects.all().order_by('id')
    avatar = ProfileAvatar.objects.get_or_create(related_user=user)
    avatar = ProfileAvatar.objects.get(related_user=user)
    context['user'] = user
    context['contacts'] = contacts
    context['avatar'] = avatar
    return render(request, "home/user.html", context)


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'home/change.html', {'form': form})

    
@login_required()
def chat(request, pk):
    # current user
    user_info = User.objects.get(id=request.user.id)
    # contact
    contact = User.objects.get(id=pk)
    # all messages from the current user
    message_list = Message.objects.filter(user=request.user).order_by('-received_date')[:30]
    # all messages from the contact
    response_list = Message.objects.filter(user=pk).order_by('-received_date')[:30]
    # messages show list
    ret_list = message_list.union(response_list).order_by('received_date')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            info.save()
            return HttpResponseRedirect(reverse('chat', args=(pk,)))

    form = MessageForm()
    return render(request, "home/chat.html", {'user_info': user_info, 'contact': contact, 'rets': ret_list, 'form': form,})


@login_required()
def contact_admin(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email_address': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())
            info = form.save(commit=False)
            info.user = request.user
            info.save()
            messages.success(request, "Message sent")
            try:
                send_mail(subject, message, 'admin@example.com', ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("contact")
    
    form = ContactForm()
    return render(request, "home/contact.html", {'form': form,})
