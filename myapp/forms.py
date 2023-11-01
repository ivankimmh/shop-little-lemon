from django import forms
from .models import Booking


# ModelForm: MenuForm
class MenuForm(forms.Form):
    item_name = forms.CharField(max_length=200)
    category = forms.CharField(max_length=200)
    description = forms.CharField(max_length=1000)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
