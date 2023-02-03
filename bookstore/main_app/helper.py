from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class JSONResponse(HttpResponse):
  def __init__(self, data, **kwargs):
    content = JSONRenderer().render(data)
    kwargs['content_type'] = 'application/json'
    super(JSONResponse, self).__init__(content, **kwargs)

class APIs():
  def getAll(model, serializer_model, *args, **kwargs):
    try:
      objects = model.objects.all()
      serializer = serializer_model(objects, many=True)
      return JSONResponse({'response' : serializer.data}, status=200)
    except Exception as ex:
      return JSONResponse({"error" : ex}, status=400)

  def getbyId(model, serializer_model, object_id):
    try:
      object = model.objects.filter(id = object_id)
      if not object:
        return JSONResponse({"Object not found"}, status=404)
      serializer = serializer_model(object, many=True)
      return JSONResponse({'response' : serializer.data}, status=200)
    except Exception as ex:
      return JSONResponse({"error" : ex}, status=400)

  def update(model, serializer_model, object_id, request):
    try:
      object = model.objects.get(id = object_id)
      data = JSONParser().parse(request)
      serializer = serializer_model(object, data=data)
      if serializer.is_valid():
        serializer.save()
        return JSONResponse({'response' : serializer.data}, status=200)
    except Exception as ex:
      return JSONResponse({"error" : ex}, status=400)

  def delete(model, object_id):
    try:
      object = model.objects.filter(id = object_id)
      if not object:
        return JSONResponse({"Object not found"}, status=404)
      object.delete()
      return JSONResponse({'message': 'object was deleted successfully!'}, status=200)
    except Exception as ex:
      return JSONResponse({"error" : ex}, status=400)