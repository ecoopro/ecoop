from django.contrib import admin
from models import *

admin.site.register([ Proveidor, Client, Producte, Comanda, DetallComanda, Comissio, Event ])
