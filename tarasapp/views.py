from django.shortcuts import render
from django.conf import settings
import random
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tarasapp.models import *
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

@csrf_exempt
def sendotp(request):
	response={}
	response['result']="Sorry"
	if request.method == 'POST':
		if request.POST['apikey']==settings.API_KEY:
			mobileno=request.POST['mobileno']
			try:
				up=UserProfile.objects.get(mobile=mobileno)
				up.status=0
			except:
				up=UserProfile()
			up.mobile=mobileno
			otp=random.randint(1000,9999)
			up.otp=otp
			up.save()
			postdata={}
			postdata['authkey']=settings.MSG91_AUTH_KEY
			postdata['mobiles']=request.POST['mobile']
			postdata['message']="Hello\nWelcome to TARAS API. Your OTP is "+str(otp)
			postdata['route']="4"
			postdata['sender']=settings.MSG91_SENDER_ID
			postdata['response']='json'
			output=requests.post(settings.MSG_URL,data=postdata)
			response['result']="Successfully sent otp"
			response['success']="1"
		else:
			response['result']="Invalid api Key"
			response['success']="0"
	return JsonResponse(response)


@csrf_exempt
def verifyotp(request):
	response={}
	response['result']="Sorry"
	if request.method == 'POST':
		if request.POST['apikey']==settings.API_KEY:
			mobileno=request.POST['mobileno']
			try:
				up=UserProfile.objects.get(mobile=mobileno)
				if up.otp == request.POST['otp']:
					if not up.user:
						up.status=2
					else:
						up.status=1
					response['status']=str(up.status)
					up.save()
					response['success']="1"
				else:
					response['result']="Invalid otp code"
					response['success']="0"
			except:
				response['result']="Invalid mobile no"
				response['success']="0"
		else:
			response['result']="Invalid api Key"
			response['success']="0"
	return JsonResponse(response)



		



