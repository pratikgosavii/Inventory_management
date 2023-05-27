from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import *


from store.models import *


@login_required(login_url='login')
def dashboard(request):
    
    stock_data = stock.objects.all()
    print(stock_data)
    stock_count = 0
    for i in stock_data:
        stock_count = stock_count + i.total_bag
    print(stock_count)

    inward_data = inward.objects.all()
    inward_count = 0
    for i in inward_data:
        inward_count = inward_count + i.bags

    outward_data = outward.objects.all()
    outward_count = 0
    for i in outward_data:
        outward_count = outward_count + i.bags

    agent_data = agent.objects.all().count()
    context = {
        'stock': stock_count,
        'inward_count': inward_count,
        'outward_count': outward_count,
        'agent_data': agent_data
    }
    return render(request, 'dashboard.html', context)
