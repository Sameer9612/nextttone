from django.contrib import admin
from .models import (
    Model, Portfolio, Client, Booking,
    ModelApplication, Blog, CourseRegistration,
    ContactForm, ModelImage
)


# -------------------------
# Model Admin
# -------------------------
@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'height', 'get_chest_bust_display', 'waist', 'hips', 'status', 'created_at']
    list_filter = ['status', 'gender', 'chest_bust_type', 'created_at']
    search_fields = ['name']
    ordering = ['name']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'gender', 'status')
        }),
        ('Physical Details', {
            'fields': ('height', ('chest_bust_type', 'chest_bust_size'), 'waist', 'hips', 'shoe_size')
        }),
        ('Profile', {
            'fields': ('bio', 'profile_image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# -------------------------
# Portfolio Admin
# -------------------------
@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['title', 'model', 'category', 'photographer', 'shoot_date', 'is_featured']
    list_filter = ['category', 'is_featured', 'shoot_date', 'created_at']
    search_fields = ['title', 'model__name', 'photographer']


# -------------------------
# Client Admin
# -------------------------
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'client_type', 'company', 'contact_person', 'email', 'created_at']
    list_filter = ['client_type', 'created_at']
    search_fields = ['name', 'company', 'contact_person', 'email']


# -------------------------
# Booking Admin
# -------------------------
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['title', 'model', 'client', 'booking_type', 'status', 'start_date', 'rate', 'phone_number', 'email']
    list_filter = ['booking_type', 'status', 'start_date', 'created_at']
    search_fields = ['title', 'model__name', 'client__name', 'location', 'phone_number', 'email']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('model', 'client', 'booking_type', 'title', 'description')
        }),
        ('Schedule & Location', {
            'fields': ('start_date', 'end_date', 'location')
        }),
        ('Financial & Status', {
            'fields': ('rate', 'status')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email')
        }),
        ('Additional Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )


# -------------------------
# Model Application Admin
# -------------------------
@admin.register(ModelApplication)
class ModelApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "name", "email", "phone", "age", "city", "country", "height",
        "bust_chest", "waist", "hips", "shoe", "instagram", "data_policy"
    ]
    readonly_fields = ("photo1", "photo2", "photo3")
    search_fields = ("name", "email", "phone", "instagram")
    list_filter = ("country", "city", "age", "height", "data_policy")


# -------------------------
# Blog Admin
# -------------------------
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content', 'meta_title', 'meta_description', 'meta_keywords']
    list_filter = ('status', 'created_on', 'author')
    date_hierarchy = 'created_on'
    raw_id_fields = ('author',)


# -------------------------
# Course Registration Admin
# -------------------------
@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'course_type', 'state', 'created_at']
    list_filter = ['course_type', 'state', 'created_at']
    search_fields = ['full_name', 'email']


# -------------------------
# Contact Form Admin
# -------------------------
@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'ip_address']


# -------------------------
# Model Image Admin
# -------------------------
class ModelImageInline(admin.TabularInline):
    model = ModelImage
    extra = 4
    max_num = 4
    fields = ['image', 'caption', 'order']


@admin.register(ModelImage)
class ModelImageAdmin(admin.ModelAdmin):
    list_display = ['model', 'order', 'created_at']
    list_filter = ['model', 'created_at']
    ordering = ['model', 'order']


# -------------------------
# Customize Admin Site Titles
# -------------------------
admin.site.site_header = "NEXTTTONE ADMIN"
admin.site.site_title = "NEXTTTONE ADMIN"
admin.site.index_title = "Welcome to NEXTTTONE GLOBAL MODELING AGENCY ADMIN"
