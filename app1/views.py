from django.http import *
import datetime
from django.shortcuts import *
from ayuda import *
from app1.models import *
from django.views.decorators.http import require_http_methods
from django.contrib import auth
from django.contrib.auth.views import login, logout
from django.contrib.sessions.middleware import SessionMiddleware

# Create your views here.
#return render_to_response('sometemplate.html')

def basic(request):
    return HttpResponse("Hello world")


def data_hora(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

#def clients(request):
#    clients = Client.objects.order_by('nom_client')
#    context = {"clients":clients}
#    return render(request,'clients.html',context)

def thanks(request):
    return render_to_response('thanks.html')


def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })


def prova(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    else:
        #print request.session.get('nom_usuari_ses')
        if request.method == 'POST': # If the form has been submitted...
            form1 = ClientForm(request.POST) # A form bound to the POST data
            if form1.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                # ara haurem de redireccionar cap a un altre web via post li pasem el valor de l'usuari.
                #a = request.POST.get("valor")
                _id = request.POST.get("valor")
                return HttpResponseRedirect('/fes_comanda?id='+str(_id))
                #return HttpResponse(y.objects.order_by('client')) # Redirect after POST
        else:
            form1 = ClientForm() # An unbound form

        return render(request, 'prova.html', {
            'form': form1,
        })


#@require_http_methods(["POST"])
def fes_comanda(request):
    client_id = request.GET.get("id")
    #return HttpResponse(id)
    if request.method == 'POST': # If the form has been submitted...
        form = FesComandaForm(request.POST) # A form bound to the POST data

        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            client_id = form.cleaned_data['client_id']
            client = Client.objects.filter(ref_client=client_id)
            id_producte = form.cleaned_data['productes']
            producte = Producte.objects.filter(ref_prod=id_producte)
            quantitat = form.cleaned_data['quantitat']
            data_entrega = form.cleaned_data['data_entrega']
            #user_ses  = request.session['usuari']
            

            for x in client:
                nom_client = x.nom_client

            for x in producte:
                producte = x.nom_prod
            dic={'client' : client_id, 'producte': producte, 'quantitat':quantitat, 'data_entrega':data_entrega}
            grabar_comanda(dic)

            context= {'client':nom_client, 'producte':producte, 'id_producte':id_producte, 'quantitat':quantitat, 'data':data_entrega }
            #return HttpResponseRedirect('/') # Redirect after POST
            #return HttpResponse(client_id producte quantitat data_entrega)
            return render(request, 'veure_comandes.html', context)
    else:
        form = FesComandaForm() # An unbound form
        #print(id) # element de testing
    form.fields['client_id'].widget=forms.HiddenInput()
    form.fields['client_id'].initial=client_id
    return render(request, 'fes_comanda.html', {
        'form': form,
    })
    #pass

def comanda(request):
    id_client = request.GET.get("id")
    context = {'comandes':torna_comandes_by_client(id_client)}
    return render(request,'comandes.html',context)

def producte(request):
    productes = Producte.objects.order_by('nom_prod')
    context = {"productes":productes}
    return render(request,'producte.html',context)

def detall_comanda(request):
    detalls = DetallComanda.objects.order_by('quantitat_demnada')
    context = {"detalls":detalls}
    return render(request,'detall_comanda.html',context)


def search_form(request):
    return render(request, 'search_form.html')

def search(request):
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)


def veure_comanda(request):
    if request.method == 'POST': # If the form has been submitted...
        form = VeureComandaForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            
            # Process the data in form.cleaned_data
            # ...
            #return HttpResponseRedirect('/thanks/') # Redirect after POST
            _id = request.POST.get("valor")
            return HttpResponseRedirect('/comanda?id='+str(_id))
    else:
        form = VeureComandaForm() # An unbound form

    return render(request, 'veure_comandes.html', {
        'form': form,
    })

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        request.session['nom_usuari_ses'] = 'username'
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/loggedout/")