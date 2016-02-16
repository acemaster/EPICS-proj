from django.shortcuts import render
from django.conf import settings
import random
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def sendmessage(request):
	response={}
	response['result']="Sorry"
	if request.method == 'POST':
		otp=random.randint(1000,9999)
		postdata={}
		postdata['authkey']=settings.MSG91_AUTH_KEY
		postdata['mobiles']=request.POST['mobile']
		postdata['message']="This is a test message"
		postdata['route']="4"
		postdata['sender']=settings.MSG91_SENDER_ID
		postdata['response']='json'
		output=requests.post(settings.MSG_URL,data=postdata)
		response['result']=output.content
	return JsonResponse(response)
		



