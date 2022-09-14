from django import forms
from django.forms import ModelForm, Textarea
from django.core import validators
from eye.models import Item, Organization, Orgbranch, ItemType, ItemModel, Location, Event, EventType, InfoPrinter, InfoUPS, InfoPC
from django.utils.translation import ugettext as _

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['name']

class QRForm(forms.Form):
    number = forms.DecimalField(label=_('Number of QR codes:'), min_value=1, max_digits=4)

class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'), )
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

class OrgbranchForm(ModelForm):
    organization   = forms.ModelChoiceField(label=_('Organization'), queryset=Organization.objects.all(), required = True)
    class Meta:
        model = Orgbranch
        fields = ['organization','name','address']

class ItemTypeForm(ModelForm):
    class Meta:
        model = ItemType
        fields = ['name']

class InfoPrinterForm(ModelForm):
    qprints = forms.DecimalField(label=_('number of printz:'), min_value=1)
    class Meta:
        model = InfoPrinter
        fields = ['qprints']

class InfoUPSForm(ModelForm):
    test_result = forms.CharField(label=_("Test result:"))
    test_date            = forms.DateTimeField(
            label=_('Last test date:'), 
            input_formats=['%d/%m/%Y %H:%M'],
            required = True,
            widget=forms.DateTimeInput(attrs={'class': 'datetime'})
            )
    replace_date         = forms.DateTimeField(
            label=_('Last battery replace date:'), 
            input_formats=['%d/%m/%Y %H:%M'],
            required = True,
            widget=forms.DateTimeInput(attrs={'class': 'datetime'})
            )
    class Meta:
        model = InfoUPS
        fields = ['replace_date','test_date','test_result']

class InfoPCForm(ModelForm):
    service_date            = forms.DateTimeField(
            label=_('Last service date:'), 
            input_formats=['%d/%m/%Y %H:%M'],
            required = True,
            widget=forms.DateTimeInput(attrs={'class': 'datetime'})
            )
    class Meta:
        model = InfoPC
        fields = ['service_date']

class LocationForm(ModelForm):
    organization   = forms.ModelChoiceField(label=_('Organization'), queryset=Organization.objects.all(), required = True)
    orgbranch      = forms.ModelChoiceField(label=_('Orgbranch'), queryset=Orgbranch.objects.all() , required = True)
    class Meta:
        model = Location
        fields = ['organization','orgbranch','name']

class ItemModelForm(ModelForm):
    type       = forms.ModelChoiceField(label=_("Itemtype"),queryset=ItemType.objects.all(), required = False)
    class Meta:
        model = ItemModel
        fields = ['type','name']

class EventForm(ModelForm):
    eventtype       = forms.ModelChoiceField(label=_('Eventtype'),queryset=EventType.objects.all(), required = True)
    date            = forms.DateTimeField(
            label=_('Date'), 
            input_formats=['%d/%m/%Y %H:%M'],
            required = True,
            widget=forms.DateTimeInput(attrs={'class': 'datetime-inline'})
            )
    #description     = forms.Textarea(label=_('Description'), )
    description     = forms.Textarea( )
    item            = forms.CharField(widget=forms.HiddenInput)
    class Meta:
        model = Event
        fields = ['eventtype','date','description','item']
        #???
#        widgets = {
#                'item': forms.HiddenInput(),
#                }

class ItemForm(ModelForm):
     organization   = forms.ModelChoiceField(label=_('Organization'), required = True, queryset=Organization.objects.all())
     orgbranch      = forms.ModelChoiceField(label=_('Orgbranch'), required = True,queryset=Orgbranch.objects.all())
     itemtype       = forms.ModelChoiceField(label=_('Itemtype'), required = True,queryset=ItemType.objects.all())
     location       = forms.ModelChoiceField(label=_('Location'), required = True,queryset=Location.objects.all())
     served         = forms.BooleanField(label=_('Served'), required = False)
     model          = forms.ModelChoiceField(label=_('Model'), required = True,queryset=ItemModel.objects.all())
     description    = forms.CharField(
             label=_('Description'), 
             required = False,
             widget=forms.Textarea(attrs={'cols':50, 'class':'u-full-width'})
             )
     class Meta:
        model = Item
        fields = ['organization','orgbranch','location','model','itemtype','description','served']

class SearchItemForm(ItemForm):
     showempty   = forms.BooleanField(label=_('Show empty:'), required = False)
     item_id   = forms.CharField(label=_('Organization ID:'), required = False)
     served    = forms.BooleanField(widget=forms.CheckboxInput(attrs={'checked' : 'checked', 'id':'someshit'}),required = False)
     class Meta(ItemForm.Meta):
        exclude = ('description',)
     def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['organization'].required = None
        self.fields['orgbranch'].required = None
        self.fields['location'].required = None
        self.fields['itemtype'].required = None
        self.fields['model'].required = None
     
class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'), )
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
