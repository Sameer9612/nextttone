from django import forms
from .models import ModelApplication, CourseRegistration, ContactForm


# -------------------------
# Model Application Form
# -------------------------
class ModelApplicationForm(forms.ModelForm):
    data_policy = forms.BooleanField(
        label="I accept the privacy policy*",
        required=True
    )

    class Meta:
        model = ModelApplication
        fields = [
            'name', 'phone', 'email', 'city', 'country', 'age',
            'height', 'bust_chest', 'waist', 'hips', 'shoe',
            'instagram', 'photo1', 'photo2', 'photo3', 'data_policy'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'First Last'}),
            'phone': forms.TextInput(attrs={'placeholder': '0123 456789'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Age'}),
            'height': forms.TextInput(attrs={'placeholder': 'Height (e.g. 178cm)'}),
            'bust_chest': forms.TextInput(attrs={'placeholder': 'Bust/Chest (e.g. 90cm)'}),
            'waist': forms.TextInput(attrs={'placeholder': 'Waist (e.g. 62cm)'}),
            'hips': forms.TextInput(attrs={'placeholder': 'Hips (e.g. 90cm)'}),
            'shoe': forms.TextInput(attrs={'placeholder': 'Shoe Size (e.g. 42)'}),
            'instagram': forms.TextInput(attrs={'placeholder': 'instagram_handle'}),
        }


# -------------------------
# Course Registration Form
# -------------------------
class CourseRegistrationForm(forms.ModelForm):
    class Meta:
        model = CourseRegistration
        fields = ['full_name', 'email', 'phone', 'course_type', 'state']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs.update({
            'required': True,
        })
        self.fields['email'].widget.attrs.update({
            'required': True,
        })
        self.fields['phone'].widget.attrs.update({
            'type': 'tel',
            'required': True,
        })
        self.fields['course_type'].widget.attrs.update({
            'required': True,
        })
        self.fields['course_type'].empty_label = "Course Type*"
        self.fields['state'].widget.attrs.update({
            'required': True,
        })
        self.fields['state'].empty_label = "Select State*"


# -------------------------
# Contact Form
# -------------------------
class ContactFormForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'required': True,
                'style': 'padding: 10px; font-size: 15px; border: 1px solid #ccc; border-radius: 4px; width: 100%; box-sizing: border-box;'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your Email',
                'required': True,
                'style': 'padding: 10px; font-size: 15px; border: 1px solid #ccc; border-radius: 4px; width: 100%; box-sizing: border-box;'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Your Message',
                'rows': 5,
                'required': True,
                'style': 'padding: 10px; font-size: 15px; border: 1px solid #ccc; border-radius: 4px; width: 100%; box-sizing: border-box; resize: vertical;'
            }),
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message
