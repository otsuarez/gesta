# vim: ai ts=4 sts=4 et sw=4

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from gesta.dnsadmin.models import Zone, Server, ZoneForm, Record, RecordForm, TTL, ProfileForm, PassForm, RecordType
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.views import login
from django.contrib.auth.models import User
# aqui se podria ajustar lo que se esta importando..
# os.mkdir, os.path
# re.match
#import re, os, errno
import re, os

def OwnedZones(username):
    u = get_object_or_404(User,username=username)
    if username == 'admin':
	return  Zone.objects.select_related().order_by("name")
    else:
	return Zone.objects.filter(owner=u).order_by("name")

def CheckZoneOwner(zid,username):
    u = get_object_or_404(User,username=username)
    z = get_object_or_404(Zone,pk=zid)
    if z.owner == u:
    	return True
    else:
    	return False
	

def logout_view(request):
    logout(request)
        # Redirect to a success page.
    return render_to_response('registration/logged_out.html',)

#@login_required
def index(request):
    username = request.user.username 
    u = get_object_or_404(User,username=username)
    #zones_list = Zone.objects.all()
    zones_list = OwnedZones(username)
    #return render_to_response('dns/index.html', {'zones_list': zones_list,'username':username})
    return render_to_response('dns/index.html', {'zones_list': zones_list,'username':username,'user':u})
index = login_required(index)

def custom_500_view(request):
	username = request.user.username 
	u = get_object_or_404(User,username=username)
	zones_list = OwnedZones(username)
	message = "La accion ejecutada genero un error. El administrador ha sido notificado."
	return render_to_response('dns/index.html', {'zones_list': zones_list,'username':username,'user':u,'message':message})

def custom_404_view(request):
	username = request.user.username 
	u = get_object_or_404(User,username=username)
	zones_list = OwnedZones(username)
	message = "El recurso solicitado no existe"
	return render_to_response('dns/index.html', {'zones_list': zones_list,'username':username,'user':u,'message':message})

def user_edit(request,uid):
	u = get_object_or_404(User,pk=uid)
	user_action = "edit"
	#up = get_object_or_404(UserProfile,pk=u.id)
	if request.method == 'POST':
		#form = ZoneForm(request.POST,instance=z)
		form = ProfileForm(request.POST,instance=u)
		user_action = "status"
		if form.is_valid():
			form.save()
			message = "Perfil Actualizado" 
			#return HttpResponseRedirect(reverse('gesta.dnsadmin.views.zone_list', args=[zid]))
		else:
			message = "Configuracion de su Perfil" 
		return render_to_response('dns/user.html',{'message': message,'user':u,'user_action':user_action})
	else:
		message = "Configuracion de su Perfil" 
		#form = ZoneForm(instance=z)
		#        form = ZoneForm()
		form =  ProfileForm(instance=u)
		return render_to_response('dns/user.html',{'message': message,'user':u,'user_action':user_action,'form':form})
	#return render_to_response('dns/user.html', {'form': form, 'message': message,'zid':zid})    

def user_pass(request,uid):
	u = get_object_or_404(User,pk=uid)
	user_action = "pass"
	if request.method == 'POST':
		form = PassForm(request.POST)
		if form.is_valid():
			user = authenticate(username=u.username, password=request.POST['oldpass'])
			if user is not None:
				#print "You provided a correct username and password!"
				newpass = request.POST['newpass']
				u.set_password(newpass)
				u.save()
			else:
				print "Your username and password were incorrect."
			user_action = "status"
			message = "Perfil Actualizado" 
			#return HttpResponseRedirect(reverse('gesta.dnsadmin.views.zone_list', args=[zid]))
		else:
			message = "Configuracion de su Perfil" 
		return render_to_response('dns/user.html',{'message': message,'user':u,'user_action':user_action})
	else:
		message = "Configuracion de su Perfil" 
		#form = ZoneForm(instance=z)
		#        form = ZoneForm()
		form =  PassForm()
		return render_to_response('dns/user.html',{'message': message,'user':u,'user_action':user_action,'form':form})
	#return render_to_response('dns/user.html', {'form': form, 'message': message,'zid':zid})    

def user_status(request,uid):
	u = get_object_or_404(User,pk=uid)
	user_action = "status"
	#up = get_object_or_404(UserProfile,pk=u.id)
	if request.method == 'POST':
		#form = ZoneForm(request.POST,instance=z)
		if form.is_valid():
			form.save()
			#return HttpResponseRedirect(reverse('gesta.dnsadmin.views.zone_list', args=[zid]))
		else:
			message = "Configuracion de su Perfil" 
			return render_to_response('dns/index.html',{'message': message,'user':u})
	else:
		message = "Configuracion de su Perfil" 
		#form = ZoneForm(instance=z)
		#        form = ZoneForm()
		return render_to_response('dns/user.html',{'message': message,'user':u,'user_edit':user_edit,'zone_total':OwnedZones(u.username).count()})
	return render_to_response('dns/user.html',{'message': message,'user':u,'user_action':user_action})
	#return render_to_response('dns/user.html',{'message': message,'user':u})

# --------------------------------------------------------------- #
""" 
zone_file_new
esta funcion recibe una zona y el usuario y a partir de ahi, crea lo que haga falta.
es todo lo relacionado en cuanto a files con una nueva zona
de z toma los datos de la zona - mainly z.name
""" 
def zone_file_new(z,username):
	# primero creamos el fichero de la zona con los datos que tenemos: soa
	# zone data file
	zone_file_zone_new(z,username)
	# segundo creamos el fichero .conf de la zona
	zone_file_conf_new(z,username)

def zone_file_zone_new(z,username):
	# anteprimero, chequeamos que ese usuario tenga creado su dir - por ahora hace falta ...
	# 	cuando el usuario se cree y sus carpetas tambien, esto no hara falta...
	#zdfiledir = settings.ROOT_DNSFILES_ZONES+username[0]+'/'+username
	s = Server.objects.all()
	zdfiledir = settings.APP_DIR+s[0].fqdn+settings.MASTERDNSFILES_ZONES+username[0]+'/'+username
	if not os.path.exists( zdfiledir ):
		os.mkdir(zdfiledir)
	zdfilename = zdfiledir+'/'+z.name+'.db'
	zone_file_zone_write(z,username,zdfilename)

def zone_file_zone_write(z,username,zdfilename):
	zdfile =  open(zdfilename,"w")
	zdfile.write(zone_file(z))
	zdfile.close()


"""
esta funcion es casi identica a zone_file_conf_create(username,zones_list):
solo que esta recibe una sola zona y la otra recibe un listado completo
lo dejo asi por ahora ...
"""
def zone_file_conf_new(z,username):
	#zdfiledir = settings.ROOT_DNSFILES_ZONES+username[0]+'/'+username
	#zcfiledir = settings.ROOT_DNSFILES_INCLUDESDIR+username[0]
	s = Server.objects.all()
        master_zcfiledir = settings.APP_DIR+s[0].fqdn+settings.CONFDNSFILES_INCLUDESDIR+username[0] 
	slave_zcfiledir = settings.APP_DIR+s[1].fqdn+settings.CONFDNSFILES_INCLUDESDIR+username[0]
	#zcfilename = zcfiledir+'/'+username+'.conf'
        master_zcfilename = master_zcfiledir+'/'+username+'.conf' 
	slave_zcfilename = slave_zcfiledir+'/'+username+'.conf'
	#if not os.path.exists( zcfiledir ):
	#	os.mkdir(zcfiledir)
	if not os.path.exists( master_zcfiledir ):
		os.mkdir(master_zcfiledir)
	if not os.path.exists( slave_zcfiledir ):
		os.mkdir(slave_zcfiledir)
	#if not os.access(zcfilename, os.F_OK):
	#	zcfile =  open(zcfilename,"w")
	#	#zcfile.write(zone_file_soa_data())
	#	zcfile.close()
	if not os.access(master_zcfilename, os.F_OK):
		master_zcfile =  open(master_zcfilename,"w")
	#	master_zcfile.close()
	else:
		master_zcfile =  open(master_zcfilename,"a")
	if not os.access(slave_zcfilename, os.F_OK):
		slave_zcfile =  open(slave_zcfilename,"w")
	#	slave_zcfile.close()
	else:
		slave_zcfile =  open(slave_zcfilename,"a")
	#zcfile =  open(zcfilename,"a")
	#if not
	#data = '\n'
	#data +=  'zone "'+z.name+'" {\n'
	#data += '\ttype master;\n'
	#data += '\tfile "masters/'+username[0]+'/'+username+'/'+z.name+'.db";\n'
	#data += '};\n' 
	master_data = slave_data = '\n'
	master_data +=  'zone "'+z.name+'" {\n' 
	slave_data +=  'zone "'+z.name+'" {\n' 
	master_data += '\ttype master;\n' 
	slave_data += '\ttype slave;\n' 
	master_data += '\tfile "masters/'+username[0]+'/'+username+'/'+z.name+'.db";\n' 
	slave_data += '\tfile "slaves/'+username[0]+'/'+username+'/'+z.name+'.db";\n' 
	slave_data += '\tmasters {'+s[0].ip_address+';  };\n' 
	master_data += '};\n' 
	slave_data += '};\n' 
	master_zcfile.write(master_data) 
	slave_zcfile.write(slave_data)
	#zcfile.write(data)
	#zcfile.close()
        master_zcfile.close() 
	slave_zcfile.close()

"""
esta funcion no hace falta pues el named protesta si defines mas de un options
y ya esta en el named.conf
"""
def zone_file_soa_data():
	data =  'options {\n'
	data +=  '\tdirectory "'+settings.CHROOT_DNSFILES_ZONES+'";\n'
	data += '};\n'
	return data
""" 
def zone_file_conf_create(u):
para borrar una zona del fichero de configuracion tenia dos opciones:
1. borrar el fichero y regenerarlo a partir de las zonas del usuario
2. parsear el fichero, borrar la zona y regenerarlo
la 1. trabaja con sql, la 2. con i/o, prefiero sql que es nativo en django
llamo esta funcion solo con el usuario porque ya la zona esta borrada
por ahora se llama desde zone_del
... en realidad, necesito mas el zones_list y el username
me ahorro un query extra...
def zone_file_conf_create(owner,zones_list):
""" 
#def zone_file_conf_create(username,zones_list):
	#zones_list = OwnedZones(u.name)
	# asumo que ya el fichero esta creado ...  gracias a zone_file_conf_new
	#  esto lo tengo que cambiar ... por un path que me refleje el servername
	# ROOT_DNSFILES_INCLUDESDIR  =  '/opt/sites/chroot/etc/includes/'
	# zcfiledir = settings.ROOT_DNSFILES_INCLUDESDIR+username[0]
	#APP_DIR  =  '/opt/sites/chroot/'

def zone_file_conf_create(username,zones_list):
	s = Server.objects.all()
	# como son solo 2 servidores por ahora, s[0] es el master y s[1] el slave EOF
	master_zcfiledir = settings.APP_DIR+s[0].fqdn+settings.CONFDNSFILES_INCLUDESDIR+username[0]
	slave_zcfiledir = settings.APP_DIR+s[1].fqdn+settings.CONFDNSFILES_INCLUDESDIR+username[0]
	#zcfilename = zcfiledir+'/'+username+'.conf'
	master_zcfilename = master_zcfiledir+'/'+username+'.conf'
	slave_zcfilename = slave_zcfiledir+'/'+username+'.conf'
	#zcfile =  open(zcfilename,"w")
	master_zcfile =  open(master_zcfilename,"w")
	slave_zcfile =  open(slave_zcfilename,"w")
	for z in zones_list:
		master_data = slave_data = '\n' 
		master_data += '# zone_file_conf_create\n'
		slave_data += '# zone_file_conf_create\n'
		master_data +=  'zone "'+z.name+'" {\n' 
		slave_data +=  'zone "'+z.name+'" {\n' 
		master_data += '\ttype master;\n'
		slave_data += '\ttype slave;\n'
		master_data += '\tfile "masters/'+username[0]+'/'+username+'/'+z.name+'.db";\n'
		slave_data += '\tfile "slaves/'+username[0]+'/'+username+'/'+z.name+'.db";\n'
		slave_data += '\tmasters {'+s[0].ip_address+';  };\n'
		master_data += '};\n'
		slave_data += '};\n'
		master_zcfile.write(master_data)
		slave_zcfile.write(slave_data)
	master_zcfile.close()
	slave_zcfile.close()

	

def zone_file_zone_del(username,zname):
	#zfilename  = settings.ROOT_DNSFILES_ZONES+username[0]+'/'+username+'/'+zname+'.db'
	s = Server.objects.all()
	# como son solo 2 servidores por ahora, s[0] es el master y s[1] el slave EOF
	# los ficheros de zona solo se crean en el master
	master_zfilename = settings.APP_DIR+s[0].fqdn+settings.MASTERDNSFILES_ZONES+username[0]+'/'+username+'/'+zname+'.db'
	if os.access(master_zfilename, os.F_OK):
		os.remove(master_zfilename)

""" 
def zone_file_conf_new:
def zone_file_zone_new:
def zone_file_del:
def zone_file_zone_del:
def zone_file_conf_del:
""" 

""" 
def zone_exists(name):
    owner = request.user.username
    if z.owner == u:
        return True
    else:
        return False
""" 
	

def zone_add(request):
    owner = request.user.username
    if request.method == 'POST':
	u = get_object_or_404(User,username=owner) 
	z = Zone()
	z.owner = u 
	zones_list = OwnedZones(owner)
	if Zone.objects.filter(name__iexact=request.POST['name']).count():
	    message = "Ya existe una zona con ese nombre."
	    return render_to_response('dns/index.html',{'message': message,'zones_list':zones_list,'username':owner})
        form = ZoneForm(request.POST, instance=z)
        if form.is_valid():
            zone_add = '0' 
            form.save()
            message = 'Zona creada!!'
	    zone_file_new(z,owner)
	    return HttpResponseRedirect(reverse('gesta.dnsadmin.views.zone_list', args=[z.id]))
    else:
        form = ZoneForm()
	zone_add = '1' 
	zones_list = OwnedZones(owner)
       # zones_list = Zone.objects.all()
    return render_to_response('dns/index.html', {'zone_add':zone_add,'zoneform':form,'zones_list':zones_list,'username':owner})

"""
no hace nada con la zona en si, es con los registros
"""
def zone_edit(request,zid):
    if request.method == 'POST':
		z = get_object_or_404(Zone,pk=zid)
		form = ZoneForm(request.POST,instance=z)
		message = "Dominio editado exitosamente !!"			
		#form = ZoneForm(instance=z)
		#	form = ZoneForm(request.POST)
		if form.is_valid():
			form.save()
			#return HttpResponseRedirect('/')
			#return render_to_response('dns/index.html',{'message': message})
			#return render_to_response(url_redirect\,{'message': message})
			return HttpResponseRedirect(reverse('gesta.dnsadmin.views.zone_list', args=[zid]))
		else:
			message = 'los datos son invalidos'
			return render_to_response('dns/index.html',{'message': message})
    else:
		z = get_object_or_404(Zone,pk=zid)
		message = "Editando el dominio !!"
		form = ZoneForm(instance=z)
		#        form = ZoneForm()
    return render_to_response('dns/zone_edit.html', {'form': form, 'message': message,'zid':zid})    

def zone_del(request,zid):
    owner = request.user.username
    if request.method == 'POST':
		form = ZoneForm(request.POST)
		z = get_object_or_404(Zone,pk=zid)
		message = "El dominio " + z.name + " fue eliminado exitosamente."
		zname = z.name
		z.delete()
		zone_del = '0'
		# fichero de la zona
		zone_file_zone_del(owner,zname)
	    	zones_list = OwnedZones(owner)
		# fichero de configuracion
		zone_file_conf_create(owner,zones_list)
		return render_to_response('dns/index.html',{'message': message,'zones_list':zones_list,'username':owner})
    else:
		form = ZoneForm()
		z = get_object_or_404(Zone,pk=zid)        
		message = 'Operacion sobre:' + z.name
		zone_del = '1' 
	    	#zones_list = Zone.objects.all()
	    	zones_list = OwnedZones(owner)
		return render_to_response('dns/index.html', {'zone_del':zone_del,'zid':zid,'zname':z.name,'zoneform':form,'zones_list':zones_list,})
	   	#return render_to_response('dns/zone_del.html', {'form': form, 'message': message,'zid':zid})   

# --------------------------------------------------------------- #
#@login_required
def zone_list(request,zid):
    owner = request.user.username
    if not  CheckZoneOwner(zid,owner): 
    	return HttpResponseRedirect('/dns/')
    u = get_object_or_404(User,username=owner)
    zones_list = OwnedZones(owner)
    if request.method == 'POST':
        form = ZoneForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Zona creada!! por suerte...'
            #zones_list = Zone.objects.all()
            zones_list = OwnedZones(owner)
            return HttpResponseRedirect('/')
    else:
        form = RecordForm()
	#zones_list = Zone.objects.all()
	#  bump! esto estaba comentareado ... y no se porque ...
        zones_list = OwnedZones(owner)
        ttl_list = TTL.objects.all()
        #record_list = Record.objects.filter(zone=zid)
        fullrr_list = Record.objects.filter(zone=zid) 
        rl_list = fullrr_list
        for rr in fullrr_list: 
            if rr.type.id == 15: 
                url_cname_rr = Record.objects.filter(zone=zid,type=6,name__iexact=rr.name)
                urlr = get_object_or_404(Record,pk=url_cname_rr[0].id)        
                rl_list = rl_list.exclude(id=urlr.id) 
        record_list = rl_list
	z = get_object_or_404(Zone,pk=zid)
	# toja
	reverse = 0
	ptrz = ''
	if 'in-addr.arpa' in z.name :
		zname = z.name 
		reverse = 1
		fullreverseip = zname.split('.') 
		# le quito el in-addr y el arpa 
		reverseip = fullreverseip[1:-2] 
		reverseip.reverse() 
		ptrz = '.'.join(reverseip)
		#freverseip = '.'.join(fullreverseip)
	return render_to_response('dns/index.html', {'zones_list':zones_list,'form':form,'zid':zid,'record_list':record_list,'zone':z,'ttl_list':ttl_list,'username':request.user.username,'user':u,'reverse':reverse,'ptrz':ptrz}) 
zone_list = login_required(zone_list)

def new_serial():
  import datetime
  return datetime.datetime.now().strftime("%Y%m%d00")


def soa_serial_update(serial):
  import datetime
  today = datetime.datetime.now().strftime("%Y%m%d")
  #today00 = datetime.datetime.now().strftime("%Y%m%d00")
  if serial[:8] == today:
  	#ya se editor hoy una vez al menos...
	incremento = "%02d" % (int(serial[8:])+1)
	return u'%s%s' % (today,incremento)
  else:
	return u'%s00' % (today)

def record_add(request,zid):
    owner = request.user.username 
    z = get_object_or_404(Zone,pk=zid)
    if request.method == 'POST':
        form = RecordForm(request.POST) 
        if form.is_valid():
            tipo = form.cleaned_data['type']
            if str(tipo) == 'URL':
                cname_rr_type = get_object_or_404(RecordType,pk='6')
                form_name = form.cleaned_data['name']
                form_ttl = form.cleaned_data['ttl']
                #cname = form_name + '.' + z.name
                rcname = Record(zone=z,name=form_name, type=cname_rr_type, value=settings.REDIRECT_HOSTNAME, ttl=form_ttl)
                rcname.save()
            form.save() 
            z.serial = soa_serial_update(z.serial) 
            z.save()
            zone_file_zone_new(z,owner)
            return HttpResponseRedirect(reverse('gesta.dnsadmin.views.zone_list', args=[zid]))
        else:
            #dad = error.ni.idea
            msg = 'Error creando registro'
            return render_to_response('dns/index.html', {'message':msg}) 
    else:
        # aqui en realidad el GET no hace nada ... 
        form = RecordForm()
    zones_list = OwnedZones(owner)
    record_list = Record.objects.filter(zone=zid)
    return render_to_response('dns/index.html', {'zones_list':zones_list,'form':form,'zid':zid,'record_list':record_list,'zone':zone}) 

def record_del(request,id):
    owner = request.user.username
    if request.method == 'POST':
        message = "Eliminando el registro !!"
        r = get_object_or_404(Record,pk=id)
        z = get_object_or_404(Zone,pk=r.zone.id)
        record_del = '0'
        if r.type.id == 15: 
            url_cname_rr = Record.objects.filter(zone=z.id,type=6,name__iexact=r.name) 
            urlr = get_object_or_404(Record,pk=url_cname_rr[0].id) 
            urlr.delete()
        r.delete()
        z.serial = soa_serial_update(z.serial) 
        z.save()
        zone_file_zone_new(z,owner)
        return HttpResponseRedirect(reverse('gesta.dnsadmin.views.zone_list', args=[z.id]))
    else:
        r = get_object_or_404(Record,pk=id)
        message = "Eliminando el registro !!" +  r.name
        record_del = '1'
        zones_list = OwnedZones(owner)
        return render_to_response('dns/index.html', {'record_del':record_del,'rid':id,'rr':r,'zones_list':zones_list,})

def dummy(zid):
        #record_list = Record.objects.filter(pk=rid)
	dada.out
	new_ttl = "working"
	return render_to_response("new_ttl")


def ttl_update(request,rid,ttlid):
	r = get_object_or_404(Record,pk=rid)
	t = get_object_or_404(TTL,pk=ttlid)
	z = get_object_or_404(Zone,pk=r.zone.id)
	z.serial = soa_serial_update(z.serial)
	z.save()
	oldttl = r.ttl.id 
	r.ttl = t
	r.save()
	response =  HttpResponse() 
	zone_file_zone_new(z,request.user.username)
	response.write(r.ttl.description)
	return response

def zone_soa(z):
	#z = get_object_or_404(Zone,pk=zid)
	rendered = render_to_string('dns/soa.tpl', { 'zone': z })
	return rendered
	#rendered = "<pre>"+rendered+"</pre>"

def zone_ns(z):
	#z = get_object_or_404(Zone,pk=zid)
	rendered = render_to_string('dns/soa.tpl', { 'zone': z })

#def clean_str(st):
#	for line in st.splitlines():
def print_file(st):
	file = open('/tmp/zonefile','wU')
	st = st.replace("\n\n","\n")
	file.writelines(st)
	file.close()
	

	
"""
file_zone
originalmente era zone_file pero
necesitaba chequear que solo el dueno de la zona pudiera listar la zona
y si le ponia el if delante a la funcion original, iba a tener que reindentar todo...
utilize el nombre viejo (mapeado en la url) para crear una funcion que tuviera un if
y llamara al codigo de la funcion original
"""
def file_zone(request,zid):
	z = get_object_or_404(Zone,pk=zid)
    	u = get_object_or_404(User,username=request.user.username)
    	#if z.owner == u:
	if CheckZoneOwner(z.id,request.user.username):
		rendered = "<pre>"
		rendered += zone_file(z)
		rendered += "</pre>"
		response =  HttpResponse() 
		response.write(rendered) 
		return response
	else:
		# el que intenta ver la zona no es el dueno de la zona
		#rendered = "error - raise 404 "
		rendered = "Error - Acceso no Autorizado "
		rendered += "user: " + request.user.username + " - zid : " + z.owner.username
		response =  HttpResponse() 
		response.write(rendered) 
		return response

def fqdn_or_ip(r):
	if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',r.value):
		return r.value
	else:
		m = re.match('(\w.*)(\.$)',r.value) 
		if m:  
			# es un fqdn, tiene un punto al final...
			return r.value
		elif r.zone.name  in r.value:
			#print "es el dominio, le toca punto al final"
			return r.value + "."
		elif '.'  in r.value:
			#print "es un fqdn, punto al final y listo"
			return r.value + "."
		else:
			#print "le falta el dominio y un punto al final" 
			return r.value +"."+ r.zone.name +"."

"""
zone_file
genera el texto del fichero de zona
"""
def zone_file(z):
	"""
	Registro SOA
	"""
	#rendered += render_to_string('dns/soa.tpl', { 'zone': z })
	rendered = render_to_string('dns/soa.tpl', { 'zone': z })
	"""
	Registros NS
	"""
	rendered += "\n"
	rendered += ";registros ns \n"
	nameservers = Server.objects.all()
	for nameserver in nameservers:
		rendered += " \t"+z.ttl.ttl+"\tIN\tNS\t"+nameserver.fqdn+".\n"
	ns_record_list = Record.objects.filter(zone=z.id).filter(type='2')
	if (ns_record_list.count()):
		for r  in ns_record_list:
		  if (r.name == '.'):
			rendered += "\t"+r.ttl.ttl+"\tIN\tNS\t"+r.value+"\n"
		  else:
			rendered += r.name+".\t"+r.ttl.ttl+"\tIN\tNS\t"+r.value+"\n"
	"""
	Registros MX
	"""
	rendered += "\n"
	rendered += ";registros mx\n"
	mx_record_list = Record.objects.filter(zone=z.id).filter(type='7')
	if (mx_record_list.count()):
		for r  in mx_record_list:
		  rvalue = fqdn_or_ip(r)
		  #rvalue = r.value
		  if (r.name == z.name):
		  #if (r.name == '.'):
			rendered += "\t"+r.ttl.ttl+"\tIN\tMX\t"+r.preference+"\t"+rvalue+"\n"
			#rendered += "\t"+r.ttl.ttl+"\tIN\tMX\t"+r.preference+"\t"+r.value+"\n"
		  else:
			rendered += r.name+".\t"+r.ttl.ttl+"\tIN\tMX\t"+r.preference+"\t"+rvalue+"\n"
			#rendered += r.name+".\t"+r.ttl.ttl+"\tIN\tMX\t"+r.preference+"\t"+r.value+"\n"
	"""
	Registros A
	"""
	rendered += "\n"
	rendered += ";registros a\n"
	a_record_list = Record.objects.filter(zone=z.id).filter(type='1')
	if (a_record_list.count()):
		for r  in a_record_list:
		  if (r.name == '.'):
			rendered += "@\t"+r.ttl.ttl+"\tIN      A       "+r.value+"\n"
		  else:
			rendered += r.name+"\t"+r.ttl.ttl+"\tIN      A       "+r.value+"\n"
	"""
	Registros PTR
	"""
	rendered += "\n"
	rendered += ";registros ptr\n"
	a_record_list = Record.objects.filter(zone=z.id).filter(type='3')
	if (a_record_list.count()):
		for r  in a_record_list:
			rendered += r.name+"\t\t\tIN      PTR       "+r.value+"\n"
	"""
	Registros CNAME
	"""
	rendered += "\n"
	rendered += ";registros cname\n"
	cname_record_list = Record.objects.filter(zone=z.id).filter(type='6')
	if (cname_record_list.count()):
		#rendered += render_to_string('dns/cname.tpl',{'record_list':cname_record_list})
		#st = render_to_string('dns/cname.tpl',{'record_list':cname_record_list})
		#rendered += st.strip()
		for r  in cname_record_list:
			rendered += r.name+"\t"+r.ttl.ttl+"\tIN      CNAME       "+r.value+".\n"
	"""
	Registros TXT
	"""
	rendered += "\n"
	rendered += ";registros txt.\n"
	txt_record_list = Record.objects.filter(zone=z.id).filter(type='5')
	if (txt_record_list.count()):
		#$rendered += render_to_string('dns/txt.tpl',{'record_list':txt_record_list})
		for r  in txt_record_list:
		  if (r.name == '.'):
			rendered += "@\t"+r.ttl.ttl+"\tIN\tTXT\t\""+r.value+"\"\n"
		  else:
			rendered += r.name+".\t"+r.ttl.ttl+"\tIN\tTXT\t\""+r.value+"\"\n"
	rendered = rendered.replace("\n\t\t\t\n","\n")
	#print_file(rendered)
	return rendered

def view_settings(request):
	msg = 'hola'
	response =  HttpResponse()
	msg += "<p>dnsfiles_dir = " + settings.DNSFILES_DIR
	msg += "<p> zonefilesformat  = " + settings.ZONEFILES_FORMAT
	msg += "<p> user: " + request.user.username
	#msg += "<p> user: " + request.user.id
	rendered = msg
	response.write(rendered)
	return response

def view_msg(request,msg):
	#msg = 'hola'
	response =  HttpResponse()
	#msg += "<p> user: " + request.user.id
	rendered = msg
	response.write(rendered)
	return response

###
# This code contains portions of:
# Copyright (c) 2006-2007, Jared Kuolt
# All rights reserved.
# 
###


class RequireLoginMiddleware(object):
    """
    Require Login middleware. If enabled, each Django-powered page will
    require authentication.
    
    If an anonymous user requests a page, he/she is redirected to the login
    page set by REQUIRE_LOGIN_PATH or /accounts/login/ by default.
    """
    def __init__(self):
        self.require_login_path = getattr(settings, 'REQUIRE_LOGIN_PATH', '/dns/accounts/login/')
    
    def process_request(self, request):
        if request.path != self.require_login_path and request.user.is_anonymous():
            if request.POST:
                return login(request)
            else:
                return HttpResponseRedirect('%s?next=%s' % (self.require_login_path, request.path))
                
