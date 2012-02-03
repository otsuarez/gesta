from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from gesta.dnsadmin.models import Zone, Server, ZoneForm, Record, RecordForm
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

def logout_view(request):
    logout(request)
        # Redirect to a success page.
    return render_to_response('registration/logged_out.html',)

@login_required
def index(request):
    zones_list = Zone.objects.all()
    return render_to_response('dns/index.html', {'zones_list': zones_list})

# --------------------------------------------------------------- #

def zone_add(request):
    if request.method == 'POST':
        form = ZoneForm(request.POST)
        if form.is_valid():
            form.save()
            zone_add = '0'
            message = 'Zona creada!!'
	    zones_list = Zone.objects.all()
	    return HttpResponseRedirect('/dns/')
    else:
        form = ZoneForm()
	zone_add = '1'
        zones_list = Zone.objects.all()
    return render_to_response('dns/index.html', {'zone_add':zone_add,'zoneform':form,'zones_list':zones_list,})
	#return render_to_response('dns/index.html', {'zones_list':zones_list,'form':form,'zid':zid,'record_list':record_list,'zone':z}) 
    #return render_to_response('dns/zone_add.html', {'form': form})

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
    if request.method == 'POST':
		form = ZoneForm(request.POST)
		z = get_object_or_404(Zone,pk=zid)
		message = "El dominio " + z.name + " fue eliminado exitosamente."
		z.delete()
		zone_del = '0'
		zones_list = Zone.objects.all() 
		return render_to_response('dns/index.html',{'message': message,'zones_list':zones_list})
		# return render_to_response('dns/index.html',{'message': message})		
		#return HttpResponseRedirect(reverse('gesta.dnsadmin.views.zone_list', args=[zid]))
		#return HttpResponseRedirect('/')
    else:
		form = ZoneForm()
		z = get_object_or_404(Zone,pk=zid)        
		message = 'Operacion sobre:' + z.name
		zone_del = '1' 
		zones_list = Zone.objects.all() 
		return render_to_response('dns/index.html', {'zone_del':zone_del,'zid':zid,'zname':z.name,'zoneform':form,'zones_list':zones_list,})
	   	#return render_to_response('dns/zone_del.html', {'form': form, 'message': message,'zid':zid})   

# --------------------------------------------------------------- #
def zone_list(request,zid):
    if request.method == 'POST':
        form = ZoneForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Zona creada!! por suerte...'
	    zones_list = Zone.objects.all()
	    return HttpResponseRedirect('/')
    else:
        form = RecordForm()
        zones_list = Zone.objects.all()
        record_list = Record.objects.filter(zone=zid)
	z = get_object_or_404(Zone,pk=zid)
	return render_to_response('dns/index.html', {'zones_list':zones_list,'form':form,'zid':zid,'record_list':record_list,'zone':z}) 

def record_add(request,zid):
    if request.method == 'POST':
	form = RecordForm(request.POST) 
        if form.is_valid():
            form.save() 
	    return HttpResponseRedirect(reverse('gesta.dnsadmin.views.zone_list', args=[zid]))
	    #return HttpResponseRedirect('/')
	else:
	    dad = error.ni.idea
	    msg = 'Error creando registro'
	    return render_to_response('dns/index.html', {'message':msg}) 
    else:
	# aqui en realidad el GET no hace nada ... 
        form = RecordForm()
        zones_list = Zone.objects.all()
        record_list = Record.objects.filter(zone=zid)
	z = get_object_or_404(Zone,pk=zid)
	return render_to_response('dns/index.html', {'zones_list':zones_list,'form':form,'zid':zid,'record_list':record_list,'zone':zone}) 

def record_del(request,id):
    if request.method == 'POST':
	message = "Eliminando el registro !!"
	r = get_object_or_404(Record,pk=id)
	zname = r.zone
	z = Zone.objects.get(name=zname)
	zid = z.id
	record_del = '0'
	r.delete()
	return HttpResponseRedirect(reverse('gesta.dnsadmin.views.zone_list', args=[zid]))
	#return HttpResponseRedirect('/')
    else:
	r = get_object_or_404(Record,pk=id)
	message = "Eliminando el registro !!" +  r.name
	record_del = '1'
		#z = get_object_or_404(Zone,pk=zid)        
		#message = 'Operacion sobre:' + z.name
	zones_list = Zone.objects.all() 
	return render_to_response('dns/index.html', {'record_del':record_del,'rid':id,'rr':r,'zones_list':zones_list,})
	#return render_to_response('dns/index.html', {'record_del':record_del,'zid':zid,'zname':z.name,'zoneform':form,'zones_list':zones_list,})
	#return render_to_response('dns/record_del.html', {'rid':id,'message':message}) 
