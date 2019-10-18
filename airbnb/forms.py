from django import forms
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Row, Column, Reset, Div

class UserForm(forms.Form):
    attrs = {'class': 'form-control'}

    username = forms.CharField(label="Username", max_length=100, widget=forms.TextInput(attrs=attrs))
    password = forms.CharField(label="Password", min_length=10, max_length=20, widget=forms.PasswordInput(attrs=attrs))


class UserRegisterForm(forms.Form):
    years_list = range(datetime.now().year - 100, datetime.now().year)
    attrs = {'class': 'form-control'}

    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs=attrs))
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs=attrs))
    password = forms.CharField(label="Password", min_length=10, max_length=20, widget=forms.PasswordInput(attrs=attrs))
    firstName = forms.CharField(label="First Name", widget=forms.TextInput(attrs=attrs))
    lastName = forms.CharField(label="Last Name", widget=forms.TextInput(attrs=attrs))
    phone = forms.RegexField(regex=r'^4\d{8}')
    birthday = forms.DateField(label="Birthday", widget=forms.SelectDateWidget(years=years_list))

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'userRegister'
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('phone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('firstName', css_class='form-group col-md-6 mb-0'),
                Column('lastName', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'birthday',
            Reset('reset', 'Reset', css_class="btn btn-default pull-left"),
            Submit('submit', 'Submit', css_class="btn btn-default pull-right")
        )

class UserInfoUpdateForm(forms.Form):
    years_list = range(datetime.now().year - 100, datetime.now().year)
    attrs = {'class': 'form-control', 'style': 'width:30%'}

    email = forms.EmailField(label="Email", max_length=100, widget=forms.TextInput(attrs=attrs))
    firstName = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs=attrs))
    lastName = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs=attrs))
    phone = forms.RegexField(regex=r'^4\d{8}', max_length=100, widget=forms.TextInput(attrs=attrs))
    birthday = forms.DateField(label="Birthday", widget=forms.SelectDateWidget(years=years_list, attrs=attrs))
    #location = forms.CharField(label="Location", max_length=100, widget=forms.TextInput(attrs=attrs))
    description = forms.CharField(label="personal description", \
                                  widget=forms.Textarea(attrs={'style': 'height:100px; width:500px'}))

    def __init__(self, *args, **kwargs):
        super(UserInfoUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = 'updateUserInfo'
        self.helper.add_input(Submit('update', 'update', css_class='btn-info'))
        self.helper.form_class = 'blueForms'


class FileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'width:30%'}))

    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'description-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'portraitUpload'
        self.helper.add_input(Submit('upload', 'upload', css_class='btn-info'))


class ListingForm(forms.Form):
    propertyType = (
        ('A', 'Apartment'),
        ('B', 'House'),
    )

    roomType = (
        ('A', 'Entire place'),
        ('B', 'Private room'),
        ('C', 'Shared room'),
    )
    attrs = {'class': 'form-control', 'style': 'width:30%'}

    property_type = forms.ChoiceField(choices=propertyType, required=True, widget=forms.Select(attrs=attrs))
    room_type = forms.ChoiceField(choices=roomType, required=True, widget=forms.Select(attrs=attrs))
    Guests = forms.IntegerField(required=True, initial=1, widget=forms.NumberInput(attrs=attrs))
    Bedrooms = forms.IntegerField(required=True, initial=1, widget=forms.NumberInput(attrs=attrs))
    Beds = forms.IntegerField(required=True, initial=1, widget=forms.NumberInput(attrs=attrs))
    Bathrooms = forms.FloatField(required=True, initial=1, widget=forms.NumberInput(attrs=attrs))
    Price = forms.DecimalField(required=True, initial=100, widget=forms.NumberInput(attrs=attrs))

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'place-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'listingStart'
        self.helper.add_input(Submit('Next', 'Next', css_class='btn-info'))


class DescriptionForm(forms.Form):
    attrs = {'class': 'form-control', 'style': 'width:30%'}

    name = forms.CharField(label="Listing title", max_length=20, widget=forms.TextInput(attrs=attrs))
    summary = forms.CharField(label="Write a quick summary of your place.", max_length=100, widget=forms.TextInput(attrs=attrs))
    neighborhood = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs))
    transit = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs))

    def __init__(self, *args, **kwargs):
        super(DescriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'place-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'description'
        self.helper.add_input(Submit('Next', 'Next', css_class='btn-info'))


class AmenitiesForm(forms.Form):
    essentials = forms.BooleanField(label="Essentials", required=False)
    air_conditioning = forms.BooleanField(label="Air conditioning", required=False)
    heat = forms.BooleanField(label="Heat", required=False)
    hair_dryer = forms.BooleanField(required=False)
    wifi = forms.BooleanField(label="Wi-Fi", required=False)
    iron = forms.BooleanField(label="Iron", required=False)
    shampoo = forms.BooleanField(label="Shampoo", required=False)
    desk = forms.BooleanField(label="Desk/workspace", required=False)

    '''kitchen = forms.BooleanField(label="Kitchen", required=False)
    washing = forms.BooleanField(label="Laundry – washing machine", required=False)
    laundry_dryer = forms.BooleanField(label="Laundry - dryer", required=False)
    parking = forms.BooleanField(label="Parking", required=False)
    gym = forms.BooleanField(label="Gym", required=False)
    pool = forms.BooleanField(label="Pool", required=False)
    lift = forms.BooleanField(label="Lift", required=False)

    fire_extinguisher = forms.BooleanField(label="Fire extinguisher", required=False)
    smoke_detector = forms.BooleanField(label="Smoke detector", required=False)
    first_aid_kit = forms.BooleanField(label="First aid kit", required=False)
    '''

    def __init__(self, *args, **kwargs):
        super(AmenitiesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'place-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'amenities'
        self.helper.add_input(Submit('Next', 'Next', css_class='btn-info'))
        self.helper.form_class = 'form_horizontal'
        self.helper.layout = Layout(
            Fieldset(
                Div('essentials', css_class='checkbox'),
                Div('air_conditioning', css_class='checkbox'),
                Div('heat', css_class='checkbox'),
                Div('hair_dryer', css_class='checkbox'),
                Div('wifi', css_class='checkbox'),
                Div('iron', css_class='checkbox'),
                Div('shampoo', css_class='checkbox'),
                Div('desk', css_class='checkbox')
            ),
        )


class SceneFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'width:30%'}))

    def __init__(self, *args, **kwargs):
        super(SceneFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'description-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'scene'
        self.helper.add_input(Submit('upload', 'upload', css_class='btn-info'))