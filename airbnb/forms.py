from django import forms
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserForm(forms.Form):
    attrs = {'class': 'form-control'}

    username = forms.CharField(label="Username", max_length=100, widget=forms.TextInput(attrs=attrs))
    password = forms.CharField(label="Password", min_length=10, max_length=20, widget=forms.PasswordInput(attrs=attrs))


class UserRegisterForm(forms.Form):
    years_list = range(datetime.now().year - 100, datetime.now().year)
    attrs = {'class': 'form-control'}

    email = forms.EmailField(label="Email", max_length=100, widget=forms.TextInput(attrs=attrs))
    username = forms.CharField(label="Username", max_length=100, widget=forms.TextInput(attrs=attrs))
    password = forms.CharField(label="Password", min_length=10, max_length=20, widget=forms.PasswordInput(attrs=attrs))
    firstName = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs=attrs))
    lastName = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs=attrs))
    phone = forms.RegexField(regex=r'^4\d{8}')
    birthday = forms.DateField(label="Birthday", widget=forms.SelectDateWidget(years=years_list))


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
        self.helper.form_id = 'description-form'
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