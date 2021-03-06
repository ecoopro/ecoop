from django import forms
from django.db import models
from app1.models import *
from django.http import HttpResponseRedirect
import datetime 
import random
import time


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class ClientForm(forms.Form):
	valor = forms.ChoiceField()
	
	def __init__(self, *args, **kwargs):
		super(ClientForm, self).__init__(*args, **kwargs)
		self.fields['valor']=forms.ChoiceField(choices=torna_clients())

class FesComandaForm(forms.Form):
	productes = forms.ChoiceField()
	quantitat=forms.FloatField(max_value=12.0)
	data_entrega = forms.ChoiceField()
	client_id = forms.IntegerField()
	
	def __init__(self, *args, **kwargs):
		super(FesComandaForm, self).__init__(*args, **kwargs)
		self.fields['productes']=forms.ChoiceField(choices=torna_productes())
		self.fields['data_entrega']=forms.ChoiceField(choices=dates_entrega())

class VeureComandaForm(forms.Form):
	valor = forms.ChoiceField()

	def __init__(self, *args, **kwargs):
		super(VeureComandaForm, self).__init__(*args, **kwargs)
		self.fields['valor']=forms.ChoiceField(choices=torna_clients())

class ReportForm(forms.Form):
	data_entrega = forms.ChoiceField()
	def __init__(self, *args, **kwargs):
		super(ReportForm, self).__init__(*args, **kwargs)
		self.fields['data_entrega']=forms.ChoiceField(choices=dates_entrega())

# ----- Funcions per aleugerir les classes -----

# Funcio que torna la llista actual de tots els productes
def torna_productes():
	prod=[]
	x=Producte.objects.order_by('ref_prod')
	for c in x:
		prod.append((c.ref_prod , c.nom_prod))
	prod=tuple(prod)
	return prod


# Funcio que torna la llista actual de tots els clients
def torna_clients():
	valor_clients=[]
	x=Client.objects.order_by('id')
	for c in x:
		valor_clients.append((c.id , c.nom_client))
	valor_clients=tuple(valor_clients)
	return valor_clients


# Funcio que genera les 4 proximes dates d'entrega per l'usuari tenint en compte el dia actual
def dates_entrega():
	divendres=divendres_tancat()
	avui = datetime.date.today()
	if divendres== True :
		avui = avui + datetime.timedelta(days=-avui.weekday() + 1, weeks=2) #si avui es passat dv la comanda sera per d'aqui 2 setmanes
	else:
		avui = avui + datetime.timedelta(days=-avui.weekday() + 1, weeks=1) # si avui encara no es dv la comanda es pot fer per la proxima setmana
	dates_entrega = []
	dates_entrega.append((str(avui), str(avui)))
	dates_entrega.append((str(avui+datetime.timedelta(weeks=1)), str(avui+datetime.timedelta(weeks=1))))
	dates_entrega.append((str(avui+datetime.timedelta(weeks=2)), str(avui+datetime.timedelta(weeks=2))))
	dates_entrega.append((str(avui+datetime.timedelta(weeks=3)), str(avui+datetime.timedelta(weeks=3))))
	dates_entrega=tuple(dates_entrega)
	return dates_entrega


# Funcio que torna si avui es dv per saber si encara es pot realitzar la comanda per el proxim dimarts  (relacionat amb funct dates_entrega)
def divendres_tancat(): #comprova si avui es diendres per saber si encara es pot fer la comanda per la proxima setmana o per d'aui 2 setmanes
	#avui = datetime.datetime(2013, 12, 21) #nomes per simular que avui es dv
	avui=datetime.date.today() #agafa el dia actual 
	if avui.weekday()>4:
		return True
	else:
		return False
"""
def torna_client_by_id(id):
	client=Client.objects.filter(ref_client='15')
	return client
"""
def torna_comandes_by_client(id_client):
	llista_comandes=[]
	#client = torna_client_by_id(id_client)
	client_sel = Client.objects.filter(id=id_client)
	comandes = Comanda.objects.filter(client=client_sel[0])
	#comandes = Comanda.objects.filter(client=client.id)
	for comanda in comandes:
		#if comanda.client.id == client_sel[0].id:
			llista_comandes.append(comanda)
	#llista_comandes=tuple(llista_comandes)

	return llista_comandes


#dic={client_id : client_id, producte: producte, quantitat:quantitat, data_entrega:data_entrega}
def grabar_comanda(dic):
	#client = 15
	#prod = 15
	#quantitat = 10
	#data_entrega = 2014-01-14 
	data = '10012014'
	data_creacio_comanda= datetime.datetime.strptime(data, "%d%m%Y").date()
	ref_com=random.randint(0,299)
	client_inst= Client.objects.filter(id=dic['client'])
	new_comanda = Comanda(ref_comanda=ref_com, data_entreaga_comanda=dic['data_entrega'], client=client_inst[0],data_creacio_comanda=data_creacio_comanda,data_recollida_comanda=dic['data_entrega'])
	new_comanda.save()
	# per fer comandes s'han d'insertar tots els camps 
	prod = Producte.objects.filter(ref_prod=dic['id_producte'])
	quantitat_d = dic['quantitat']
	quantitat_e = 0

	new_detall_comanda= DetallComanda(producte=prod[0], quantitat_demnada=quantitat_d, quantitat_entregada=quantitat_e, comanda=new_comanda)
	new_detall_comanda.save()

	#codi tret des del terminal 
	#	data = datetime.datetime.strptime('14042014', "%d%m%Y").date()
	#	new_comanda = Comanda(ref_comanda=ref_com, data_entreaga_comanda=data, client=client_inst[0],data_creacio_comanda=data,data_recollida_comanda=data)


def total_productes_report(lista):
	lista_comandes=lista
	lista_det=[]
	dic={}
	lista_final=[]
	lista_dic=[]
	resultat={}
	#ara agafem els objectes detallcomanda
	for x in lista_comandes:
		lista_det.append(DetallComanda.objects.filter(comanda=x))
	#ara lista_det es una llista amb tots els detall de comandes 

	#
	for a in lista_det:	
		if a[0].producte.nom_prod in dic:
			dic[a[0].producte.nom_prod] += a[0].quantitat_demnada
		else:
			dic.update({a[0].producte.nom_prod:a[0].quantitat_demnada})

	for v in dic:
		a = Producte.objects.filter(nom_prod=v)
		# v # retora el nom del producte
		# dic[v] #retorna la quantitat del producte
		# a[0].proveidor_prod.nom_prov #retorna el nom del proveidor
		
		lista_final.append(a[0].proveidor_prod.nom_prov)
		lista_final.append(v)
		lista_final.append(dic[v])

	# ara tenim una lista de valors semplant a aixo [u'Mango', 11.0, u'Casa Caritat', u'patata', 2.0, u'Casa Caritat']

	for i in range(0, len(lista_final), 3):
	    if lista_final[i] in resultat:
	        resultat[lista_final[i]].update({lista_final[i+1]:lista_final[i+2]})
	    else:
	       resultat.update({lista_final[i]:{lista_final[i+1]:lista_final[i+2]}})

	# ara tenim les dades en aquet format  sera molt mes facil treballar
	return resultat

	#.producte.proveidor_prod tornar el proveidor.


