from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from tasks.models import Task, UserProfile


class UserAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        if self.fields["username"].label is None:
            self.fields["username"].label = capfirst(self.username_field.verbose_name)

        self.fields["username"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"
        self.fields["password"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"


class UserCreationFormCustom(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"
        self.fields["password1"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"
        self.fields["password2"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True


class ModifyMailTimeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.fields["mail_time"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"
        # self.fields["minute"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"
        # hour = forms.IntegerField()
        # minute = forms.IntegerField()
        mail_time = forms.CharField(widgets=forms.TimeInput)

    class Meta:
        model = UserProfile
        fields = ("mail_time",)  # "minute")
        # widgets = {"mail_time": forms.TimeInput(attrs={"type": "time"})}


class TaskCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"
        self.fields["description"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"
        self.fields["status"].widget.attrs["class"] = "p-4 m-4 bg-gray-200/75"

    def clean_title(self):  # Format: create_<field>
        title = self.cleaned_data["title"]

        if len(title) == 0:
            raise ValidationError("Title is required")

        return title

    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "status",
        )
