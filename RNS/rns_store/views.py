# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

import base64,gzip,ast,cv2
from django.http import HttpResponse, JsonResponse
import numpy as np
from rns_store.serializers import StoreSerializer
from rns_store.models import Store
from .packages import save_logo

@api_view(["POST"])
def CreateStore(request):
	if request.method == "POST":
		print('pass')
		name=request.POST.get("name")
		description=request.POST.get("description")
		tags=request.POST.get("tags")
		img_shape = ast.literal_eval(request.POST.get("shape"))
		buffer = base64.b64decode(request.POST.get("logo").encode())
		logo = np.frombuffer(buffer, dtype=np.uint8).reshape(img_shape)
		path_logo=save_logo.save(logo)
        
		store_data = {
            "name":name,
            "description":description,
            "logo":path_logo,
            "tags":tags,
            "likes":1,
            }
		store_serializer = StoreSerializer(data=store_data)
		if store_serializer.is_valid():
			store_serializer.save()
            
		return JsonResponse(
			{"class": "Data store"},safe=False,)
@api_view(["POST"])
def DeleteStore(request):
	if request.method == "POST":
            name = request.POST.get("name")
            try:
            	Store.objects.filter(name=name).delete()
            except Store.DoesNotExist:
                return JsonResponse({"data": ["data not exist"]})  
            return JsonResponse({"save": 'deleted'}, safe=False)
@api_view(["GET"])
def GetStorelist(request):
	if request.method == "GET":

            try:
                get_list = Store.objects.filter(
                    name=request.GET.get("name")
                ).values()
            except Store.DoesNotExist:
                return JsonResponse({"data": ["data not exist"]})
            # print(list(get_list))
            if list(get_list) != []:
                logo_path = get_list[0]["logo"]
                logo = cv2.imread(logo_path)
                # img_b64 = base64.b64encode(img)
                logo_b64 = base64.b64encode(logo).decode()
                
                # data = {"data": list(get_list), "image": logo_b64, "shape": logo.shape}
                # data = img_b64.decode("utf-8")
                return JsonResponse({"img": logo_b64, "shape": logo.shape, "data": list(get_list)}
                	,safe=False,)
            return JsonResponse({"data": 'data not found'}, safe=False)
            # return JsonResponse({"data": list(image_data)}, safe=False)
