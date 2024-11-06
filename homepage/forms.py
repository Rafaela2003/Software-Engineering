import os

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from .models import Item, Author
from django.forms import formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


def validate_image(file):
    # Define allowed image extensions
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
    file_extension = os.path.splitext(file.name)[1].lower()

    # Check if the file extension is in the allowed list
    if file_extension[1:] not in allowed_extensions:
        raise ValidationError(
            f"Unsupported file extension: {file_extension}. Allowed extensions are: {', '.join(allowed_extensions)}")


class MultipleFileField(forms.FileField):
    # A file field to handle multiple image uploads

    def __init__(self, *args, **kwargs):
        class MultipleFileInput(forms.ClearableFileInput):
            allow_multiple_selected = True

        kwargs.setdefault("widget",
                          MultipleFileInput(attrs={
                              "id": "upload_images",
                              "accept": ".jpg, .jpeg, .png, .gif"  # Restrict file types
                          }))  # Set HTML id to bind event listener
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if isinstance(data, (list, tuple)):
            files = []
            for d in data:
                file = super().clean(d, initial)
                if file:
                    validate_image(file)
                    files.append(file)
            return files
        else:
            file = super().clean(data, initial)
            if file:
                validate_image(file)
            return file


class SearchForm(forms.Form):
    # user search form, applies to home page

    title = forms.CharField(required=False, label="Title")
    author = forms.CharField(required=False, label="Photographer")
    tag = forms.CharField(required=False, label="Tags")
    datefrom = forms.DateField(required=False, label="From")
    dateto = forms.DateField(required=False, label="to")
    files_Still_Images = forms.BooleanField(initial=True, label="Still images")
    file_RTI = forms.BooleanField(initial=True, label="Reflectance Transformation Imaging files")
    # files_3d = forms.BooleanField(initial=True, label="Three-dimensional objects (.obj & .mtl, etc.)")


from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div
from datetime import datetime
from django.conf import global_settings


# from froala_editor.widgets import FroalaEditor


class ItemInfoForm(forms.Form):
    # upload form, applies to upload page

    Title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Title of your project'}),
        label='Title'
    )
    Upload_Images = MultipleFileField()
    Author = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Name of photographer'}),
        label='Photographer'
    )
    Upload_Date = forms.DateField(
        required=True,
        initial=timezone.now,
        widget=forms.DateInput(attrs={'type': 'date', 'max': str(datetime.now().date())}),
        label='Upload Date'
    )
    IsRti = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'IsRti'}),
        label='Add RTI File'
    )
    Description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'description', 'rows': 3}),
        label='Description'
    )  # new
    Alternate_Title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Alternate Title'}),
        label='Alternate Title'
    )
    Language = forms.ChoiceField(
        choices=[('', 'Select Language')] + list(global_settings.LANGUAGES),
        required=False,
        widget=forms.Select(),
        label='Language'
    )
    # Email = forms.EmailField(
    #    required=False,
    #    widget=forms.TextInput(attrs={'placeholder': '123@abc.com'}),
    #    label='Email'
    # )
    Provenance = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Provenance'}),
        label='Provenance'
    )
    Current_Collection_Location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Location'}),
        label='Current Collection Location'
    )
    Dimensions = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Dimensions'}),
        label='Dimensions'
    )
    Accession_Number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Number'}),
        label='Accession Number'
    )
    Tags = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Enter Tags separated by commas', 'rows': 2}),
        label='Tags'
    )
    # Install editor to add hypertext form
    Bibliography = forms.CharField(
        required=False,
        # widget=FroalaEditor(),
        widget=forms.Textarea(attrs={'placeholder': 'Enter Tags separated by commas', 'rows': 5}),
        label='Bibliography'
    )


'''Remove
    def __init__(self, *args, **kwargs):
        super(ItemInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('Title', css_class='form-group col-md-10 mb-20'),
                css_class='form-row'
            ),
            Row(
                Column('Author', css_class='form-group col-md-10 mb-20',id='author-fields'),
                css_class='form-row'
            ),
            #Add 'Add Author' button in form and related js in templates
            Row(
                Div(
                    HTML('<button type="button" class="btn btn-primary" id="add-author-btn">Add Author</button>'),
                    css_class='form-group col-md-2 mb-20'
                ),
                css_class='form-row'
            ),
            Div(
                css_class='form-row',
                id='additional-authors'
            ),
            Row(
                Column('Upload_Date', css_class='form-group col-md-10 mb-20'),
                css_class='form-row'
            ),
            Row(
                Column('Upload_Images', css_class='form-group col-md-10 mb-20'),
                css_class='form-row'
            ),
            Row(
                Column('IsRti', css_class='form-group col-md-10 mb-20'),
                css_class='form-row'
            ),
            Row(
                Column('Description', css_class='form-group col-md-10 mb-20'),
                css_class='form-row'
            ),  # new
            Row(
                Div(
                    HTML(
                        '<button type="button" class="btn btn-primary" data-toggle="collapse" data-target="#tagsCollapse" aria-expanded="false" aria-controls="tagsCollapse">Advanced</button>'),
                    css_class='form-group col-md-2 mb-20'
                ),
                css_class='form-row'
            ),  # new
            Div(
                Row(
                    Column('Alternate_Title', css_class='form-group col-md-5 mb-20'),
                    Column('Language', css_class='form-group col-md-5 mb-20'),
                    css_class='form-row'
                ),
                #Row(
                #    Column('Email', css_class='form-group col-md-10 mb-20'),
                #    css_class='form-row'
                #),
                Row(
                    Column('Provenance', css_class='form-group col-md-10 mb-20'),
                ),
                Row(
                    Column('Current_Collection_Location', css_class='form-group col-md-10 mb-20'),
                ),
                Row(
                    Column('Dimensions', css_class='form-group col-md-10 mb-20'),
                ),
                Row(
                    Column('Accession_Number', css_class='form-group col-md-10 mb-20'),
                ),
                Row(
                    Column('Tags', css_class='form-group col-md-10 mb-20'),
                ),
                Row(
                    Column('Bibliography', css_class='form-group col-md-10 mb-20'),
                ),
                css_class='collapse',
                id='tagsCollapse'
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary col-md-10')
        )
'''


class EditForm(forms.ModelForm):
    # upload form, applies to upload page

    Title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Title of your project'}),
        label='Title'
    )
    Upload_Images = MultipleFileField(
        required=False,
        label='Add Images')
    Author = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Name of photographer'}),
        label='Photographer'
    )
    Upload_Date = forms.DateField(
        required=True,
        initial=timezone.now,
        widget=forms.DateInput(attrs={'type': 'date', 'max': str(datetime.now().date())}),
        label='Upload Date'
    )
    IsRti = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'IsRti'}),
        label='Add or Re-upload RTI File'
    )
    Description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'description', 'rows': 3}),
        label='Description'
    )  # new

    Alternate_Title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Alternate Title'}),
        label='Alternate Title'
    )
    Language = forms.ChoiceField(
        choices=[('', 'Select Language')] + list(global_settings.LANGUAGES),
        required=False,
        widget=forms.Select(),
        label='Language'
    )
    # Email = forms.EmailField(
    #    required=False,
    #    widget=forms.TextInput(attrs={'placeholder': '123@abc.com'}),
    #    label='Email'
    # )
    Provenance = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Provenance'}),
        label='Provenance'
    )
    Current_Collection_Location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Location'}),
        label='Current Collection Location'
    )
    Dimensions = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Dimensions'}),
        label='Dimensions'
    )
    Accession_Number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Number'}),
        label='Accession Number'
    )
    Tags = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Enter Tags separated by commas', 'rows': 2}),
        label='Tags'
    )
    # Install ckeditor to add hypertext form
    Bibliography = forms.CharField(
        required=False,
        # widget=FroalaEditor(),
        widget=forms.Textarea(attrs={'placeholder': 'Enter Tags separated by commas', 'rows': 5}),
        label='Bibliography'
    )

    class Meta:
        model = Item
        fields = [
            'Title',
            'Author',
            'Upload_Date',
            # 'Email',
            'Description',
            'Alternate_Title',
            'Tags',
            'Language',
            'Provenance',
            'Current_Collection_Location',
            'Dimensions',
            'Accession_Number',
            'Bibliography',
        ]


'''Remove
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('Title', css_class='form-group col-md-10 mb-20'),
                css_class='form-row'
            ),
            Row(
                Column('Author', css_class='form-group col-md-10 mb-20', id='author-fields'),
                css_class='form-row'
            ),
            # Add 'Add Author' button in form and related js in templates
            Row(
                Div(
                    HTML('<button type="button" class="btn btn-primary" id="add-author-btn">Add Author</button>'),
                    css_class='form-group col-md-2 mb-20'
                ),
                css_class='form-row'
            ),
            Div(
                css_class='form-row',
                id='additional-authors'
            ),
            Row(
                Column('Upload_Date', css_class='form-group col-md-10 mb-20'),
                css_class='form-row'
            ),
            Row(
                Column('Upload_Images', css_class='form-group col-md-10 mb-20'),
                css_class='form-row'
            ),
            Row(
                Column('IsRti', css_class='form-group col-md-10 mb-20'),
                css_class='form-row'
            ),
            Row(
                Column('Description', css_class='form-group col-md-10 mb-20'),
                css_class='form-row'
            ),  # new
            Row(
                Div(
                    HTML(
                        '<button type="button" class="btn btn-primary" data-toggle="collapse" data-target="#tagsCollapse" aria-expanded="false" aria-controls="tagsCollapse">Advanced</button>'),
                    css_class='form-group col-md-2 mb-20'
                ),
                css_class='form-row'
            ),  # new
            Div(
                Row(
                    Column('Alternate_Title', css_class='form-group col-md-5 mb-20'),
                    Column('Language', css_class='form-group col-md-5 mb-20'),
                    css_class='form-row'
                ),
                #Row(
                #    Column('Email', css_class='form-group col-md-10 mb-20'),
                #    css_class='form-row'
                #),
                Row(
                    Column('Provenance', css_class='form-group col-md-10 mb-20'),
                ),
                Row(
                    Column('Current_Collection_Location', css_class='form-group col-md-10 mb-20'),
                ),
                Row(
                    Column('Dimensions', css_class='form-group col-md-10 mb-20'),
                ),
                Row(
                    Column('Accession_Number', css_class='form-group col-md-10 mb-20'),
                ),
                Row(
                    Column('Tags', css_class='form-group col-md-10 mb-20'),
                ),
                Row(
                    Column('Bibliography', css_class='form-group col-md-10 mb-100'),
                ),
                css_class='collapse',
                id='tagsCollapse'
            ),
            Submit('submit', 'Submit', css_class='btn btn-primary col-md-10')
        )
'''


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    is_uploader = forms.BooleanField(required=False, help_text="Allow this user to upload items.")
    is_superuser = forms.BooleanField(required=False, help_text="Designate this user as a superuser.")

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2', 'first_name', 'last_name',
            'is_uploader', 'is_superuser'
        ]


class LoginForm(AuthenticationForm):
    # username = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'autofocus': True}))
    # password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput)
    username = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
