from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import EmailValidator, MinLengthValidator
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


# -------------------------
# Model for Modeling Agency
# -------------------------
class Model(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB', 'Non-Binary'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
    ]

    CHEST_BUST_TYPE_CHOICES = [
        ('C', 'Chest'),
        ('B', 'Bust'),
    ]

    name = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    height = models.DecimalField(max_digits=4, decimal_places=1, help_text="Height in cm")

    chest_bust_type = models.CharField(max_length=1, choices=CHEST_BUST_TYPE_CHOICES, default='C')
    chest_bust_size = models.DecimalField(max_digits=4, decimal_places=1, default=90.0, help_text="Chest/Bust in cm")
    waist = models.DecimalField(max_digits=4, decimal_places=1, default=75.0, help_text="Waist in cm")
    hips = models.DecimalField(max_digits=4, decimal_places=1, default=95.0, help_text="Hips in cm")
    shoe_size = models.CharField(max_length=10, default="7")

    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='models/profiles/', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('model-view', args=[str(self.id)])

    def get_chest_bust_display(self):
        return f"{self.get_chest_bust_type_display()}: {self.chest_bust_size}cm"


# -------------------------
# Portfolio for Models
# -------------------------
class Portfolio(models.Model):
    CATEGORY_CHOICES = [
        ('fashion', 'Fashion'),
        ('commercial', 'Commercial'),
        ('beauty', 'Beauty'),
        ('editorial', 'Editorial'),
        ('lifestyle', 'Lifestyle'),
    ]

    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='portfolio')
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='portfolio/')
    description = models.TextField(blank=True)
    photographer = models.CharField(max_length=100, blank=True)
    shoot_date = models.DateField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.model.name}"


# -------------------------
# Client Model
# -------------------------
class Client(models.Model):
    CLIENT_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('agency', 'Agency'),
        ('brand', 'Brand'),
        ('photographer', 'Photographer'),
    ]

    name = models.CharField(max_length=100)
    client_type = models.CharField(max_length=15, choices=CLIENT_TYPE_CHOICES)
    company = models.CharField(max_length=100, blank=True)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -------------------------
# Booking Model
# -------------------------
class Booking(models.Model):
    BOOKING_TYPE_CHOICES = [
        ('photoshoot', 'Photoshoot'),
        ('runway', 'Runway Show'),
        ('commercial', 'Commercial'),
        ('event', 'Event'),
        ('campaigns', 'Campaigns'),
        ('ugc_influencer', 'UGC & Influencer Content'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='bookings')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bookings')
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPE_CHOICES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.model.name}"


# -------------------------
# Model Application Form
# -------------------------
class ModelApplication(models.Model):
    name = models.CharField("Name*", max_length=100)
    phone = models.CharField("Mobile Number*", max_length=20)
    email = models.EmailField("E-Mail*", max_length=100)
    city = models.CharField("City*", max_length=100)
    country = models.CharField("Country*", max_length=100)
    age = models.PositiveIntegerField("Age*")
    height = models.CharField("Height*", max_length=30)
    bust_chest = models.CharField("Bust / Chest*", max_length=30, blank=True, null=True)
    waist = models.CharField("Waist*", max_length=30, default="N/A")
    hips = models.CharField("Hips*", max_length=30, default="N/A")
    shoe = models.CharField("Shoe*", max_length=30, default="N/A")
    instagram = models.CharField("Instagram (username)", max_length=100, blank=True)

    photo1 = models.ImageField("Photo #1*", upload_to="model_photos/")
    photo2 = models.ImageField("Photo #2*", upload_to="model_photos/")
    photo3 = models.ImageField("Photo #3 (optional)", upload_to="model_photos/", blank=True, null=True)
    data_policy = models.BooleanField("Privacy Policy*", default=False)

    def __str__(self):
        return self.name


# -------------------------
# Blog Model
# -------------------------
class Blog(models.Model):
    STATUS_CHOICES = [
        (0, "Draft"),
        (1, "Publish"),
    ]

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)
    summary = models.CharField(max_length=300, blank=True)
    content = CKEditor5Field("Content", config_name="default")
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=250, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


# -------------------------
# Course Registration
# -------------------------
class CourseRegistration(models.Model):
    COURSE_CHOICES = [
        ('essence', 'NTA ESSENCE'),
        ('vision', 'NTA VISION'),
        ('couture', 'NTA COUTURE'),
        ('connect', 'NTA CONNECT'),
    ]

    STATE_CHOICES = [
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CT', 'Chhattisgarh'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JK', 'Jammu and Kashmir'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Odisha'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TG', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UT', 'Uttarakhand'),
        ('WB', 'West Bengal'),
        ('AN', 'Andaman and Nicobar Islands'),
        ('CH', 'Chandigarh'),
        ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('DL', 'Delhi'),
        ('LD', 'Lakshadweep'),
        ('PY', 'Puducherry'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    course_type = models.CharField(max_length=20, choices=COURSE_CHOICES)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='DL')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.get_course_type_display()}"

    class Meta:
        verbose_name = "Course Registration"
        verbose_name_plural = "Course Registrations"
        ordering = ['-created_at']


# -------------------------
# Contact Form Model
# -------------------------
class ContactForm(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)], help_text="Enter your full name")
    email = models.EmailField(validators=[EmailValidator()], help_text="Enter a valid email address")
    message = models.TextField(validators=[MinLengthValidator(10)], help_text="Enter your message (minimum 10 characters)")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Form Submission"
        verbose_name_plural = "Contact Form Submissions"

    def __str__(self):
        return f"{self.name} - {self.email} ({self.get_status_display()})"

    def mark_as_read(self):
        self.status = 'read'
        self.save()

    def mark_as_replied(self):
        self.status = 'replied'
        self.save()

    def mark_as_closed(self):
        self.status = 'closed'
        self.save()


# -------------------------
# Model Slideshow Images
# -------------------------
class ModelImage(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='slideshow_images')
    image = models.ImageField(upload_to='models/slideshow/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Order in slideshow")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Model Image"
        verbose_name_plural = "Model Images"

    def __str__(self):
        return f"{self.model.name} - Image {self.order + 1}"
