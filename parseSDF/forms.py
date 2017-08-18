import django.forms as forms


class UploadFile(forms.Form):
    file = forms.FileField(required=True)
