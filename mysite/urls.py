"""home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the 'include()' function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from home import views
from myapp import views as myapp_views
from chat import views as chat_views
from rest_framework import routers


# register APIs
router = routers.DefaultRouter()
router.register(r'contacts', views.ContactView, 'contacts')
router.register(r'choices', myapp_views.ChoiceView, 'choices')
router.register(r'questions', myapp_views.QuestionView, 'questions')

# urls
urlpatterns = [
    path('hereis-the-admin-loggin-page9527-li/', admin.site.urls),
    path('hereis-the-api-page7054-li/', include(router.urls)),
    path('', views.home_response, name='home'),
    path('myapp/', include('myapp.urls')),
    path('pillrecognition/', include('pillrecognition.urls')),
    path('users/', views.user_response, name='user'),
    path('users/<int:pk>/', views.chat, name='chat'),
    path('users/contact', views.contact_admin, name='contact'),
    path('users/change_password', views.change_password, name='change_password'),
    path('users/edit_profile', chat_views.edit_account_view, name='edit_profile'),
    path('users/edit_avatar', chat_views.edit_avatar_view, name='edit_avatar'),
    path('accounts/', include('allauth.urls')),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.register_request, name='register'),
    path("password_reset/", views.reset_request, name="reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='home/reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="home/reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='home/reset_complete.html'),
         name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
