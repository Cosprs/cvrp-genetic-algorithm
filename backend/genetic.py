from django.http import HttpResponse

from cvrp.src.genetic import run


def genetic(request):
    return HttpResponse(run(
        capacity=int(request.GET.get('capacity', 10)),
        points=int(request.GET.get('points', 100)),
        individuals=int(request.GET.get('individuals', 50)),
        replace=int(request.GET.get('replace', 25)),
        generations=int(request.GET.get('generations', 500))
    ), content_type="application/json")
