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
from django.contrib.auth.models import User
#from gesta.dnsadmin.views import user_dirs_create, user_conf_create
from django.conf import settings
from django.db.models import signals
from django.dispatch import dispatcher
import re, os, errno


class Setup(models.Model):
    name = models.CharField('Nombre',max_length=240)
    value = models.CharField('Valor',max_length=240)
    class Admin:
        list_display = ('name',)
    class Meta:
        verbose_name = 'Variable'
        verbose_name_plural = 'Setup'

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

def default_owner():
  return user.id
	

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
    owner = models.ForeignKey(User,related_name = 'owner')
    class Admin:
        list_display = ('name','owner')
	list_filter = ['owner','master']
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
    value = models.CharField(max_length=128)
    preference = models.CharField(max_length=2, blank=True)    
    ttl = models.ForeignKey(TTL, default=ttl_2h)
    class Admin:
        list_display = ('name','type','value','ttl')
	list_filter = ['type','zone']
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

class UserProfile(models.Model):
    domainslimit = models.PositiveIntegerField('Limite de Dominios',default=20)
    recordslimit = models.PositiveIntegerField('Registros por Dominios',default=20)
    first_name = models.CharField('Nombre',max_length=20)
    last_name = models.CharField('Apellidos',max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    user = models.ForeignKey(User, unique=True)
    class Admin:
        list_display = ('first_name','last_name')

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def save(self):
        #print "Antes del save(self)"+self.first_name
	if not user.id:
          	user = User.objects.create_user(self.username,'email','sha1$0eb77$6cee4d48c815149503cdb3a85e78426d7818ede5')
        	user.first_name = first_name
        	user.last_name = last_name
        	user.save()
        	self.user = user
	else:
        	user.first_name = first_name
        	user.last_name = last_name
        user.save()
        super(Person, self).save() # Call the "real" save() method
        user.set_password(password)
        user.save()
        #print "After save"+self.first_name

    def delete(self):
        #print "Before deletion"+self.first_name
        u = User.objects.get(pk=self.user.id)
        u.delete()
        super(Person, self).delete() # Call the "real" delete() method
        #print "After deletion"+self.first_name

class ProfileForm(ModelForm):
    first_name = forms.CharField(label='Nombre',required=False)
    last_name = forms.CharField(label='Apellidos',required=False)
    #password = forms.CharField(label='Contrase&ntilde;a',required=False)
    email = forms.CharField(label='Su email',required=False)
    class Meta:
            model = User
	    fields = ('first_name','last_name','email')
	    #fields = ('name', 'master')


class PassForm(ModelForm):
    oldpass = forms.CharField(label='Actual')
    newpass = forms.CharField(label='Nueva')
    class Meta:
            model = User
	    fields = ('oldpass','newpass')
	    #fields = ('name', 'master')

def user_created(instance):
  # instance is the new user
  # first let's check if this is a newly created user...
  # ROOT_DNSFILES_INCLUDESDIR  =  '/opt/sites/chroot/etc/includes/'
  #CONFDNSFILES_INCLUDESDIR  =  '/etc/includes/'
  #FILENAME = settings.ROOT_DNSFILES_INCLUDESDIR+instance.username[0]+'/'+instance.username+'.conf'
  # aqui se crean solo ficheros en el master
  s=Server.objects.get(pk=1)
  s2=Server.objects.get(pk=2)
  base_dir2 = settings.APP_DIR+s2.fqdn 
  base_dir = settings.APP_DIR+s.fqdn
  DIRNAME = base_dir+settings.CONFDNSFILES_INCLUDESDIR+instance.username[0]+'/'+instance.username 
  FILENAME = DIRNAME+'.conf'
  if not os.path.exists(FILENAME):
  	user_dirs_create(instance,base_dir)
  	user_conf_create(instance,base_dir)
	user_conf_create_slave(instance,base_dir2)


dispatcher.connect(user_created, signal=signals.post_save, sender=User)
#dispatcher.connect(user_deleted, signal=signals.pre_delete, sender=User)

# --------------- file stuff ----------------------- #
# nsfqdn - nameserver FQDN
# ---------------
# solo para el master, en el slave se crean automaticamente las carpetas y ficheros
def  user_dirs_create(instance,base_dir):
#crear directorio para los ficheros de zona:
# var/devel/sites/chroot/var/named/masters/p/pepe/
#APP_DIR  =  '/opt/sites/chroot/'
#MASTERDNSFILES_ZONES =  '/var/named/masters/'
  DIRNAME = base_dir+settings.MASTERDNSFILES_ZONES+instance.username[0]+'/'+instance.username 
  try:
# os.makedirs will also create all the parent directories
      os.makedirs(DIRNAME)
  except OSError, err:
      if err.errno == errno.EEXIST:
          if os.path.isdir(DIRNAME):
              print "directory already exists"
          else:
              print "file already exists, but not a directory"
              raise # re-raise the exception
      else:
          raise

def  user_conf_create(instance,base_dir):
# crear fichero de configuracion para las zonas del usuario:
# /var/devel/sites/chroot/etc/includes/p/pepe.conf
  DIRNAME = base_dir+settings.CONFDNSFILES_INCLUDESDIR+instance.username[0]+'/'
  FILENAME = DIRNAME+instance.username+'.conf'
  try:
      # os.makedirs will also create all the parent directories
      os.makedirs(DIRNAME)
  except OSError, err:
      if err.errno == errno.EEXIST:
          if os.path.isdir(DIRNAME):
              print "directory already exists"
          else:
              print "file already exists, but not a directory"
              raise # re-raise the exception
      else:
          raise
  # toja1
  f = open(FILENAME,"a+")
  addline = '#options {\n'
  # NAMEDFILES_DIR =  '/var/named/'
  addline += '#\t\tdirectory "'+settings.NAMEDFILES_DIR+'";\n'
  addline += '#};\n'
  f.write(addline)
  f.close()
# incluir la linea con el fichero de configuracion en el include del sitio
# /var/devel/sites/chroot/etc/example.conf
# include "/var/devel/sites/chroot/etc/includes/p/pepe.conf"
  #CONFFILENAME = settings.ROOT_DNSFILES_CONF+'/exampledns.conf'
  # en buena ley seria asi:
  #CONFFILENAME = settings.APP_DIR+'etc/exampledns.conf'
  CONFFILENAME = base_dir+'/etc/exampledns.conf'
  g = open(CONFFILENAME,"r+") 
  tk = 1
  igot = g.readlines()
  for line in igot:
  	if line.find(instance.username) > -1:
		tk = 0
  # CONFFILES_INCLUDESDIR  =  '/etc/includes/'
  #addline += '# dentro de signals\n' 
  if (tk == 1):
  	# no estaba el usuario en exampledns.conf 
	addline = 'include "'+settings.CONFFILES_INCLUDESDIR+instance.username[0]+'/'+instance.username+'.conf";\n' 
	g.write(addline) 
  g.close()

def  user_conf_create_slave(instance,base_dir):
# crear fichero de configuracion para las zonas del usuario en el slave:
  DIRNAME = base_dir+settings.CONFDNSFILES_INCLUDESDIR+instance.username[0]+'/'
  FILENAME = DIRNAME+'/'+instance.username+'.conf'
  try:
      # os.makedirs will also create all the parent directories
      os.makedirs(DIRNAME)
  except OSError, err:
      if err.errno == errno.EEXIST:
          if os.path.isdir(DIRNAME):
              print "directory already exists"
          else:
              print "file already exists, but not a directory"
              raise # re-raise the exception
      else:
          raise
  # toja1
  f = open(FILENAME,"a")
  addline = '#options {\n'
  # NAMEDFILES_DIR =  '/var/named/'
  addline += '#\t\tdirectory "'+settings.NAMEDFILES_DIR+'";\n'
  addline += '#};\n'
  f.write(addline)
  f.close()
