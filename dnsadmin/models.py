# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.newforms import ModelForm
from django import newforms as forms


class Server(models.Model):
    ip_address = models.IPAddressField(blank=True, null=True)
    fqdn = models.CharField('Servidor',max_length=240)
    note = models.CharField('Nota',max_length=240)
    class Admin:
        list_display = ('fqdn','ip_address',)

    def __unicode__(self):
            return self.fqdn

class TTL(models.Model):
    ttl = models.CharField(max_length=18)
    description = models.CharField('Descripcion',max_length=18)
    class Admin:
        list_display = ('description','ttl')
    class Meta:
        verbose_name = 'TTL'
        verbose_name_plural = 'TTLs'

    def __unicode__(self):
            return self.description

def ttl_2d(): 
  return TTL.objects.get(ttl='86400') 

def ttl_1d(): 
  return TTL.objects.get(ttl='28800') 

def ttl_2h(): 
  return TTL.objects.get(ttl='7200') 

def ttl_1w(): 
  return TTL.objects.get(ttl='604800') 

class RecordType(models.Model):
    name = models.CharField(max_length=240)
    description = models.CharField(max_length=240)
    class Admin:
        list_display = ('name','description')
    class Meta:
        verbose_name = 'Record Type'
        verbose_name_plural = 'Record Types'
   
    def __unicode__(self):
            return self.name

def record_a(): 
  return RecordType.objects.get(name='A') 

def record_mx(): 
  return RecordType.objects.get(name='MX') 

def record_cname(): 
  return RecordType.objects.get(name='CNAME') 

def record_ns(): 
  return RecordType.objects.get(name='NS') 

def new_serial():
  import datetime
  return datetime.datetime.now().strftime("%Y%m%d00")

def server_default(): 
  s = Server.objects.all()[0]
  return s.id

class Zone(models.Model):
    name = models.CharField(max_length=240)
    master = models.ForeignKey(Server,default=server_default)
    ttl = models.ForeignKey(TTL, default=ttl_2d)
    soa_refresh =  models.ForeignKey(TTL,related_name = 'soa_refresh', default=ttl_1d)
    soa_retry = models.ForeignKey(TTL, related_name = 'soa_retry', default=ttl_2h)
    soa_expiry = models.ForeignKey(TTL, related_name = 'soa_expiry', default=ttl_1w)
    soa_minimun = models.ForeignKey(TTL, related_name = 'soa_minimun', default=ttl_2d)
    soa_email = models.CharField(max_length=240,default = 'hostmaster')
    serial = models.CharField(max_length=10,default=new_serial)
    class Admin:
        list_display = ('name',)
    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'

    def __unicode__(self):
            return self.name

class ServerModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
            return "Server #%i" % obj.fqdn

class ZoneForm(ModelForm):
    #master = forms.ModelChoiceField(queryset=Server.objects.all())
    class Meta:
            model = Zone
	    fields = ('name')
	    #fields = ('name', 'master')

class Record(models.Model):
    zone = models.ForeignKey(Zone)
    name = models.CharField(max_length=65)
    type = models.ForeignKey(RecordType)
    value = models.CharField(max_length=65)
    preference = models.CharField(max_length=2, blank=True)    
    ttl = models.ForeignKey(TTL, default=ttl_2d)
    class Admin:
        list_display = ('name','type','value')
    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'

class RecordForm(ModelForm):
    #zone = models.ForeignKey(Zone)
    zone = models.ForeignKey(Zone, editable=False)
    name = models.CharField(max_length=65)
    type = forms.ModelChoiceField(queryset=RecordType.objects.all())
    value = models.CharField(max_length=65)
    preference = models.CharField(max_length=2, blank=True)    
    ttl = forms.ModelChoiceField(queryset=TTL.objects.all())
    class Meta:
            model = Record
	    fields = ('zone','name', 'type','value','preference')
