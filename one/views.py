from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

from .models import Model, Portfolio, Booking, Client, Blog, ContactForm
from .forms import ModelApplicationForm, ContactFormForm, CourseRegistrationForm

# Home view
def home(request):
    featured_models = Model.objects.filter(status='active')[:12]
    total_models = Model.objects.filter(status='active').count()
    total_bookings = Booking.objects.filter(status='completed').count()
    total_clients = Client.objects.count()
    
    context = {
        'featured_models': featured_models,
        'total_models': total_models,
        'total_bookings': total_bookings,
        'total_clients': total_clients,
    }
    return render(request, 'home.html', context)

# Model detail view
def model_view(request, pk):
    model = get_object_or_404(Model, pk=pk)
    portfolio = Portfolio.objects.filter(model=model).order_by('-created_at')
    slideshow_images = model.slideshow_images.all()[:4]
    
    context = {
        'model': model,
        'portfolio': portfolio,
        'slideshow_images': slideshow_images,
    }
    return render(request, 'model.html', context)

# Model list view
def model_list(request):
    models = Model.objects.filter(status='active').order_by('name')
    return render(request, 'model_list.html', {'models': models})

# Model detail alias
def model_detail(request, pk):
    return model_view(request, pk)

# Booking view
def book_model(request, pk):
    model = get_object_or_404(Model, pk=pk)
    
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        client_email = request.POST.get('client_email')
        client_phone = request.POST.get('client_phone')
        booking_type = request.POST.get('booking_type')
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        location = request.POST.get('location')
        budget = request.POST.get('budget')
        
        try:
            client, created = Client.objects.get_or_create(
                email=client_email,
                defaults={
                    'name': client_name,
                    'client_type': 'individual',
                    'contact_person': client_name,
                    'phone': client_phone or '',
                    'address': location,
                }
            )
            
            start_datetime = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            end_datetime = start_datetime
            
            Booking.objects.create(
                model=model,
                client=client,
                booking_type=booking_type,
                title=title,
                description=description,
                start_date=start_datetime,
                end_date=end_datetime,
                location=location,
                rate=float(budget) if budget else 0.00,
                status='pending',
                phone_number=client_phone,
                email=client_email,
                notes=f"Booking created via website by {client_name}"
            )
            
            messages.success(request, f'Your booking request for {model.name} has been submitted successfully!')
            return redirect('model-view', pk=model.pk)
        
        except Exception as e:
            messages.error(request, 'There was an error processing your booking. Please try again.')
            return redirect('model-view', pk=model.pk)
    
    return redirect('model-view', pk=model.pk)

# Model application view
def model_application_view(request):
    if request.method == 'POST':
        form = ModelApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = ModelApplicationForm()
    return render(request, 'apply_model.html', {'form': form})

# Blog list view with search
def blog_list(request):
    blogs = Blog.objects.filter(status=1).order_by('-created_on')
    search_query = request.GET.get('search')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(summary__icontains=search_query)
        )
    return render(request, 'blog_list.html', {'blogs': blogs})

# Blog detail view
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status=1)
    blog.views += 1
    blog.save(update_fields=['views'])

    recent_posts = Blog.objects.filter(status=1).exclude(id=blog.id).order_by('-created_on')[:3]
    
    context = {
        'blog': blog,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog_detail.html', context)

# Static pages views
def nta(request):
    return render(request, 'nta.html')

def ntaessence(request):
    return render(request, 'ntaessence.html')

def ntavision(request):
    return render(request, 'ntavision.html')

def ntacouture(request):
    return render(request, 'ntacouture.html')

def ntaconnect(request):
    return render(request, 'ntaconnect.html')

def about(request):
    return render(request, 'about.html')

# Contact view
def contact(request):
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                contact.ip_address = x_forwarded_for.split(',')[0]
            else:
                contact.ip_address = request.META.get('REMOTE_ADDR')
            contact.save()
            
            try:
                send_mail(
                    subject=f'New Contact Form Submission from {contact.name}',
                    message=contact.message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('contact')
    else:
        form = ContactFormForm()
    return render(request, 'contact.html', {'form': form})

# Course registration view
def course_registration(request):
    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! We will contact you within 24 hours.')
            return redirect('course_registration')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseRegistrationForm()
    return render(request, 'registercourse.html', {'form': form})
