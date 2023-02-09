from django import forms
from .models import auctionListing, Bid
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django.urls import reverse
from crispy_forms.bootstrap import PrependedText
 


class auctionListingForm(forms.ModelForm):
    class Meta:
        model = auctionListing

        fields = ('Title','Description','Image', 'Category', 'starting_Bid', 'currentBid')
        widgets = {
            'Title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your title here', 'autofill': False}),
            'Description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Sell me the pen', 'autofill': False}),
            'Image': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a URL', 'autofill': False, 'required': False}),
            'Category': forms.Select(attrs={'class': 'form-control', 'placeholder': '', 'autofill': False, 'required': False}),
            'starting_Bid': forms.NumberInput(attrs={'class': 'form-control', 'class':"input-group-prepend", 'input-group-text': '$', 'step': 1 }),
            'datePosted': forms.DateField(),
            'currentBid': forms.NumberInput(attrs={'class': 'form-control', 'type': 'hidden', 'class':"input-group-prepend", 'input-group-text': '$', 'step': 1 }),
            
        }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        #self.helper.form_action = reverse('index')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-1 me-1'
        self.helper.field_class = 'col-lg-10 mb-3'
        self.helper.add_input(Submit('saveListing', 'Save Listing', css_class='float-end'))

class newBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['newBid']
        widgets = {
            'Bid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bid Amount', 'autofill': False, 'required': False}),
            
        }
  