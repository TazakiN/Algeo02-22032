from django import forms


class CBIRMethodForm(forms.Form):
    CBIR_CHOICES = [("color", "Color"), ("texture", "Texture")]
    cbir_method = forms.ChoiceField(
        choices=CBIR_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "switch-toggle"}),
    )
