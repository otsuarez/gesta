from django.db import models
from django import newforms as forms
#from django.forms import ModelForm
#from django import forms


# Create your models here.
class TLD(models.Model):
	tld = models.CharField(max_length=67)
	class Admin:
		list_display = ('tld',)
	class Meta:
		verbose_name = 'TLD Record'
		verbose_name_plural = 'TLD Records'
	def __unicode__(self):
		return self.tld

class CheckDomainForm(forms.Form):
    sld = forms.CharField(max_length=67)
    tld = forms.ModelChoiceField(queryset=TLD.objects.all())
'''
	class Meta:
		fields = ('tls')
		model = TLD
'''

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
