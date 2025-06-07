from django import forms
from .models import Customer, Product, Bill, BillItem

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name',  'phone', ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer name'
            }),
           
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            
        }

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['customer']
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control',
                'id': 'customer-select'
            })
        }

class BillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control product-select'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control quantity-input',
                'min': '1',
                'value': '1'
            })
        }
