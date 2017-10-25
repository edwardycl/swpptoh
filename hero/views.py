from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import HttpResponseNotFound, JsonResponse
from django.forms.models import model_to_dict
from .models import Hero
import json

def heroList(request):
    if request.method == 'GET':
        # Serialization
        return JsonResponse(list(Hero.objects.all().values()), safe=False)
    elif request.method == 'POST':
        name = json.loads(request.body.decode())['name'] # Deserialization
        new_hero = Hero(name=name)
        new_hero.save()
        return HttpResponse(status=201) # 201 is 'created' response code
    else:
        # only GET and POST methods are allowed for this url
        return HttpResponseNotAllowed(['GET', 'POST'])

def heroDetail (request, hero_id):
    hero_id = int(hero_id)
    if request.method == 'GET':
        try:
            hero = Hero.objects.get(id=hero_id)
        except Hero.DoesNotExist:
            return HttpResponseNotFound()
        return JsonResponse(model_to_dict(hero))
    elif request.method == 'PUT':
        name = json.loads(request.body.decode())['name']
        try:
            hero = Hero.objects.get(id=hero_id)
        except Hero.DoesNotExist:
            return HttpResponseNotFound()
        hero.name = name
        hero.save()
        return HttpResponse(status=204) # 'No content' response
    elif request.method == 'DELETE':
        try:
            hero = Hero.objects.get(id=hero_id)
        except Hero.DoesNotExist:
            return HttpResponseNotFound()
        hero.delete()
        return HttpResponse(status=204) # 'No content' response
    else:
        # only GET, PUT and DELETE methods are allowed for this url
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])
