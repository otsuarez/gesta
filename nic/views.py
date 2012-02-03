# Create your views here.
from gesta.nic.models import CheckDomainForm, ContactForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
import pycurl, StringIO, urllib, re, sys
#from django.newforms.models import ModelForm
from django import oldforms as forms
 
def index(request):
	sys.stderr.write('This goes to the apache error log') 
	return HttpResponse("Hello, world. You're at the nic index.")

def Check(request):
    if request.method == 'POST': # If the form has been submitted...
        checkdnsform = CheckDomainForm(request.POST) # A form bound to the POST data
        if checkdnsform.is_valid(): # All validation rules pass
			sld = checkdnsform.cleaned_data['sld']
			tld = checkdnsform.cleaned_data['tld']
			#print sld #print tld #dominios = []
			msg = "un mensaje!! la forma estuvo validada ok!" 
			tld = tld.tld 
			pf = {'sld':sld, 'tld':tld} 
			url = 'https://secure.nicline.com/cgi-bin/CGICheck.pl'
			disponibilidad = post_nic(pf,url)			
			return render_to_response('nic/check.html', {
			    'msg': msg, 'disponibilidad' : disponibilidad,
			})
    else:
        checkdnsform = CheckDomainForm() # An unbound form

    return render_to_response('nic/check.html', {
        'checkdnsform': checkdnsform,
    })

def post_nic(pf,url):
	class Resultado:
		def __init__(self):
			self.contents = ''
		def body_callback(self,buf):
			self.contents = self.contents + buf
	l = Resultado()
	c = pycurl.Curl()
	c.setopt(c.POST, 1) 
	c.setopt(c.POSTFIELDS, urllib.urlencode(pf))
	#c.setopt(c.URL, "http://127.0.0.1/uno.html")
	#url = "https://secure.nicline.com/cgi-bin/CGICheck.asp?sld="+sld+"&tld="+tld
	#url = 'https://secure.nicline.com/cgi-bin/CGICheck.pl'
	c.setopt(c.URL, url)
	c.setopt(c.WRITEFUNCTION, l.body_callback)
	c.perform()
	c.close()
	print url
	return l.contents

def ModificarDominio(request):
	distribuidor = {'log':'info@example.com','pas':'secret','dom':'example.com'}
	propietario = {'idr (opcional)':'SROW - 709074 ',
	'titr':'John Doe','empr (opcional)':'Acme','dirr':' 221b Baker Street','locr':'London','idpror':'London','cpr':'00000','idpair':'United Kingdom','emar':'info@example.com','telr':'+003 20004000','faxr':''}
	ctoadministrativo = {'nomca':'John Doe','empca':'Acme','dirca':'221b Baker Street','locca':'London','idproca':'London','cp':'00000','idpaica':'United Kingdom','emaca':'info@example.com','telca':'+003 20004000','faxca':''}
	ctotecnico = {'nomct':'John Doe','empct':'Acme','dirct':'221b Baker Street','locct':'London','idproct':'London','cpct':'00000','idpaict':'United Kingdom','emact':'info@example.com','telct':'+003 20004000','faxct':''}
	dnsprimario = {'nomdns1':'dns1.example.com','ipdns1':'69.93.127.10'}
	dnssecundario = {'nomdns2':'dns2.example.com','ipdns2':'65.19.178.10'}
	full = distribuidor
	full.update(propietario)
	full.update(ctoadministrativo)
	full.update(ctotecnico)
	full.update(dnsprimario)
	full.update(dnssecundario) 
	url = 'https://secure.nicline.com/cgi-bin/CGIModificarDominio.pl'
	disponibilidad = post_nic(full,url)
	msg = 'Modificar Dominio<p>'
	return render_to_response('nic/check.html', {'msg': msg, 'disponibilidad' : disponibilidad,})

#return HttpResponse("Hello, world. You're at the modificar dominio.")
# borrar --------------------------
def check_nic2(sld,tld):
	url = 'https://secure.nicline.com/cgi-bin/CGICheck.pl'
	response = {}
	msg = ''
	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(c.VERBOSE, 0)
	b = StringIO.StringIO()
	for dominio in tld:
		domain = sld+dominio.tld
		pf = {'sld':sld, 'tld':dominio.tld}
		c.setopt(c.POSTFIELDS, urllib.urlencode(pf))
		c.setopt(pycurl.WRITEFUNCTION, b.write)
		c.perform()
		output = b.getvalue()
		estado =  re.search(r'estado>(\d)<\/estado>',output).group(1)		
		print 'sld:'+sld+'domain:'+dominio.tld+' y ahora el estado'+estado
		response[domain]=estado
	c.close()
	for x in response.keys():
		msg += x+'--'+response[x]+'..'
	return msg

def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render_to_response('contact.html', {
        'form': form,
    })

