from django import forms

class PollingUnitResultForm(forms.Form):
    polling_unit_unique_id = forms.CharField(max_length=255)
    pdp_score = forms.IntegerField(label='PDP')
    dpp_score = forms.IntegerField(label='DPP')
    acn_score = forms.IntegerField(label='ACN')
    ppa_score = forms.IntegerField(label='PPA')
    cdc_score = forms.IntegerField(label='CDC')
    jp_score = forms.IntegerField(label='JP')
    # Add more party scores as needed
