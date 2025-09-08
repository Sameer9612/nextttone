"""
URL configuration for nexttt project.

The `urlpatterns` list routes URLs to views. For more information, see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from one.views import (
    home, model_list, model_view, model_detail, book_model,
    model_application_view, nta, ntaessence, ntavision,
    ntacouture, ntaconnect, about, contact,
    blog_list, blog_detail, course_registration
)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Home page
    path('', home, name='home'),

    # Model related URLs
    path('models/', model_list, name='model-list'),
    path('model/<int:pk>/', model_view, name='model-view'),
    path('model/<int:pk>/detail/', model_detail, name='model-detail'),
    path('model/<int:pk>/book/', book_model, name='book-model'),

    # Model application form
    path('apply/', model_application_view, name='apply_model'),

    # Course pages
    path('nta/', nta, name='nta'),
    path('ntaessence/', ntaessence, name='ntaessence'),
    path('ntavision/', ntavision, name='ntavision'),
    path('registercourse/', course_registration, name='course_registration'),
    path('ntacouture/', ntacouture, name='ntacouture'),
    path('ntaconnect/', ntaconnect, name='ntaconnect'),

    # About and contact pages
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    # Blog URLs
    path('blogs/', blog_list, name='blog_list'),
    path('blogs/<slug:slug>/', blog_detail, name='blog_detail'),

    # CKEditor integration
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
