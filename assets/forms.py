from django import forms
from .models import Asset, AssetType, Location

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'type', 'serial_number', 'purchase_date', 'value', 'status', 'location', 'responsible']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'value': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].queryset = AssetType.objects.all()
        self.fields['location'].queryset = Location.objects.all()
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
