from django import forms
from django.utils.translation import ugettext_lazy as _

class SearchForm(forms.Form):
	q = forms.CharField(label=_(u'Busca'))