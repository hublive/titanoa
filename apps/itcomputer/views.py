from django.db.models import Sum
from django.shortcuts import render, HttpResponse

# Create your views here.
from invent import models as invent_model
from basedata import models as basedata_model


def index(request):
    inventobj = invent_model.Inventory.objects.filter(warehouse__name='松江仓库').all()
    print(inventobj)
    intobj = invent_model.Inventory.objects.all().values('warehouse__name','material__name').annotate(total=Sum('cnt'))
    print(intobj)
    return render(request, 'index.html', locals())
