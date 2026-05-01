from django import forms
from .models import Donor, Recipient

blood_group_choices = [
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
]

class DonorForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True,
        required=False,
        label="Username"
    )
    blood_group = forms.ChoiceField(choices=blood_group_choices, label="Blood Group")

    class Meta:
        model = Donor
        fields = ['username', 'name', 'age', 'blood_group', 'aadhar_image', 'blood_report', 'contact']
        widgets = {
            # Accept both PDF and images for Aadhaar, same as blood_report
            'aadhar_image': forms.ClearableFileInput(attrs={'accept': '.pdf,image/*', 'class': 'form-input'}),
            'blood_report': forms.ClearableFileInput(attrs={'accept': '.pdf,image/*', 'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'disabled': 'disabled'})
        self.fields['name'].widget.attrs.update({'class': 'form-input'})
        self.fields['age'].widget.attrs.update({'class': 'form-input'})
        self.fields['blood_group'].widget.attrs.update({'class': 'form-input'})
        self.fields['contact'].widget.attrs.update({'class': 'form-input'})
        # Make uploads required for form validation
        self.fields['aadhar_image'].required = True
        self.fields['blood_report'].required = True
        if user is not None:
            self.fields['username'].initial = user.username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if username != self.fields['username'].initial:
            raise forms.ValidationError("Username does not match logged-in user.")
        # Ensure file presence explicitly in case form required fails (defense-in-depth)
        if not cleaned_data.get('aadhar_image'):
            self.add_error('aadhar_image', 'Aadhaar image is required.')
        if not cleaned_data.get('blood_report'):
            self.add_error('blood_report', 'Blood report is required.')
        return cleaned_data

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age < 18:
            raise forms.ValidationError("Donor must be at least 18 years old.")
        return age

class RecipientForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True,
        required=False,
        label="Username"
    )
    blood_group = forms.ChoiceField(choices=blood_group_choices, label="Blood Group")

    class Meta:
        model = Recipient
        fields = ['username', 'name', 'age', 'blood_group', 'aadhar_image', 'blood_report', 'contact']
        widgets = {
            'aadhar_image': forms.ClearableFileInput(attrs={'accept': '.pdf,image/*', 'class': 'form-input'}),
            'blood_report': forms.ClearableFileInput(attrs={'accept': '.pdf,image/*', 'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'disabled': 'disabled'})
        self.fields['name'].widget.attrs.update({'class': 'form-input'})
        self.fields['age'].widget.attrs.update({'class': 'form-input'})
        self.fields['blood_group'].widget.attrs.update({'class': 'form-input'})
        self.fields['contact'].widget.attrs.update({'class': 'form-input'})
        # Required for upload files
        self.fields['aadhar_image'].required = True
        self.fields['blood_report'].required = True
        if user is not None:
            self.fields['username'].initial = user.username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if username != self.fields['username'].initial:
            raise forms.ValidationError("Username does not match logged-in user.")
        if not cleaned_data.get('aadhar_image'):
            self.add_error('aadhar_image', 'Aadhaar image is required.')
        if not cleaned_data.get('blood_report'):
            self.add_error('blood_report', 'Blood report is required.')
        return cleaned_data

# Contact Us form (used by contactus_view)
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, max_length=5000)
