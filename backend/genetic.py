from django.http import HttpResponse

from cvrp.src.genetic import run

def genetic(request):
    return HttpResponse(run(), content_type="application/json")