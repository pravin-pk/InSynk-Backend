from django.shortcuts import render
from django.http import JsonResponse
import random
import time
import os
from agora_token_builder import RtcTokenBuilder
import json
from django.views.decorators.csrf import csrf_exempt

from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

cred = credentials.Certificate(os.environ.get('FIREBASE_CREDENTIALS'))
firebase_admin.initialize_app(cred)
db = firestore.client()

# Create your views here.

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')


def getToken(request):
    appId = os.environ.get('AGORA_APP_ID')
    appCertificate = os.environ.get('AGORA_APP_CERTIFICATE')
    channelName = request.GET.get('channel')
    uid = random.randint(1, 257)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    # uid = f'{channelName}-{currentTimeStamp}'
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member = {
        "name": data['name'],
        "uid": data['UID'],
        "room_name": data['room_name'],
        "inSession": True
    }
    # doc = f'{data["UID"]}-{int(time.time())}'
    db.collection(u'RoomMembers').document(data['UID']).set(member)
    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = db.collection(u'RoomMembers').document(uid).get().to_dict()

    return JsonResponse({'name':member.get('name')}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    db.collection(u'RoomMembers').document(data['UID']).update({'inSession': False})
    return JsonResponse('Member deleted', safe=False)