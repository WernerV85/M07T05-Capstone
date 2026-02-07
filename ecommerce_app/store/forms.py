from django import forms

from .models import Store


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['store_name', 'store_description', 'store_category']

    def clean_store_name(self):
        store_name = self.cleaned_data.get('store_name', '').strip()
        if not store_name:
            raise forms.ValidationError('Store name is required.')
        return store_name
