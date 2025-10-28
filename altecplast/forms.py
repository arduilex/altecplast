from django import forms
from .models import  Weighing


class WeighingForm(forms.ModelForm):
    class Meta:
        model = Weighing
        exclude = ['weighing_date', 'weighing_hours', 'weighing_type']  # Exclude date, time and type fields from the form
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control form-control-sm', 'required': True}),
            'company_non_referenced': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'company-non-referenced', 'maxlength': '50'}),
            'weighing_number': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True, 'maxlength': '20'}),
            'transporter': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'transporter', 'maxlength': '30'}),
            'origin': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'origin', 'maxlength': '30'}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'vehicle-type', 'maxlength': '20'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'license-plate', 'maxlength': '15'}),
            'gross_weight_kg': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'required': True, 'id': 'gross-weight'}),
            'tare_weight': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'required': True, 'id': 'tare-weight'}),
            'net_weight_1_kg': forms.NumberInput(attrs={'class': 'form-control form-control-sm readonly-field', 'readonly': True, 'id': 'net-weight-1'}),
            'deduction_amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'deduction-amount'}),
            'deduction_type': forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'deduction-type'}),
            'net_weight_2_kg': forms.NumberInput(attrs={'class': 'form-control form-control-sm readonly-field', 'readonly': True, 'id': 'net-weight-2'}),
            'product': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True, 'id': 'product', 'maxlength': '30'}),
            'product_type': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True, 'id': 'product-type', 'maxlength': '30'}),
            'form': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'form-field', 'maxlength': '20'}),
            'color_quality': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'color-quality', 'maxlength': '20'}),
            'packaging': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'packaging', 'maxlength': '20'}),
            'packaging_quantity': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
        }