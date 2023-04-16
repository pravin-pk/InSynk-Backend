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
# firebase_admin.initialize_app()
db = firestore.client()

# Create your views here.

def create(request):
    return render(request, 'base/create.html')

def join(request):
    return render(request, 'base/join.html')

def room(request):
    return render(request, 'base/room.html')

def generateToken(channelName):
    appId = os.environ.get('AGORA_APP_ID')
    appCertificate = os.environ.get('AGORA_APP_CERTIFICATE')
    uid = f'usr-{random.randint(1, 257)}'
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    roomId = f'{channelName}-{currentTimeStamp}'
    # uid = f'{channelName}-{currentTimeStamp}'
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return token, uid, roomId

def getToken(request):
    channelName = request.GET.get('channel')
    token, uid, roomId = generateToken(channelName)
    print(token, uid, roomId, " = getToken")

    return JsonResponse({'token': token, 'uid': uid, 'roomId': roomId}, safe=False)

def fetchRoom(request):
    roomId = request.GET.get('room_id')
    channelName = roomId.split('-')[0]
    token, uid, _ = generateToken(channelName)
    print(token, uid, roomId, " = fetchRoom")

    return JsonResponse({'token': token, 'uid': uid, 'roomId': roomId, 'room': channelName}, safe=False)


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
    db.collection(u'RoomMembers').document('PK').collection(data['roomId']).document(data['UID']).set(member)
    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    roomId = request.GET.get('room_id')

    member = db.collection(u'RoomMembers').document('PK').collection(roomId).document(uid).get().to_dict()

    return JsonResponse({'name':member.get('name')}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    db.collection(u'RoomMembers').document('PK').collection(data['room_id']).document(data['UID']).update({'inSession': False})
    return JsonResponse('Member deleted', safe=False)

@csrf_exempt
def signUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        userType = request.POST.get('userType')
        db.collection(u'Users').document(email).set({
            'username': username,
            'email': email,
            'password': password,
            'userType': userType
        })
        return JsonResponse("User created", safe=False)
    
@csrf_exempt
def signIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = db.collection(u'Users').document(email).get().to_dict()
        if user:
            if user.get('password') == password:
                return JsonResponse({'user': user}, safe=False)
            else:
                return JsonResponse({'error': 'Incorrect password'}, safe=False)
        else:
            return JsonResponse({'error': 'User does not exist'}, safe=False)
        