from app_models.models import Acc, PPU, Effect, Category
from .serializers.auth_serializers import CustomTokenObtainPairSerializer, AccSerializer
from .serializers.ppu_serializer import PPUSerializer, PPUFileUploadSerializer, ModerPPUSerializer
#from .serializers.vned_ppu_serializer import VnedPPUSerializer
from .logic import *

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view,renderer_classes, permission_classes
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets

from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
#from django.core.context_processors import csrf


import jwt
import re
import json
import datetime


class CustomObtainTokenPairView(TokenObtainPairView):
    #Login view
    permission_classes = (AllowAny, )
    serializer_class = CustomTokenObtainPairSerializer


class CreateAccView(CreateAPIView):
    #Register view
    model = Acc()
    permission_classes = [
        AllowAny
    ]
    serializer_class = AccSerializer
    

class TestView(APIView):
    #Test authentication view
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {'message': 'Hello world'}
        return Response(content)

class CreatePPUView(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)



    def post(self, request, format=None):
        token = request.headers.get('Authorization').split(' ')[1]
        info = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        #try:
        #    PPU.objects.get(title=request.data['title'])
        #    update_ppu(request)
        #except Exception as e:
            
        #    return Response({'err': "Cant find ppu with this query"})
        try:
            ppu = create_ppu(request, info)
        except:
            return Response({'err': 'ошибка создания ППУ'})

        return Response("ok")
        
    def put(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        info = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

#        try:
        ppu = PPU.objects.get(title=request.data['title'])
        if info.get('username') in ppu.owners():
            data = request.data
            data['author'] = Acc.objects.get(username=info.get('username'))
            serializer = PPUSerializer(ppu, data=request.data, partial=True)
            
            print(serializer)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                print(serializer.errors)
                #print(dir(serializer))
                return Response('Неверное значение')
        else:
            Response('You are not PPU owner')
#        except:
#            return Response('Cant find ppu with this title')

class AddFilePPUView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser, FormParser, MultiPartParser,)

    @action(detail=True, methods=['put'])
    def put(self, request):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            info = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            ppu_title = info.get('filename')
                    
            ppu = PPU.objects.get(title=ppu_title)

            if info.get('username') in ppu.owners():
                if request.FILES.get('file'):
                    ppu.file = request.FILES.get('file')
                    ppu.save()

                    return Response('Файл сохранен')
                else:
                    return Response('Файл не найден')
            else:
                return Response('ППУ принаддежит не вам, так что вы не можете его редактировать')


        except:
            return Response("ППУ с этим именем уже существует")



class ListCheckingPPUs(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PPUSerializer
    model = PPU
    queryset = PPU.objects.filter(status=1)


    def get(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            info = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            acc = Acc.objects.get(username=info.get('username'))
            if acc.is_moder:
                return self.list(request, *args, **kwargs)
            else:
                return Response({'err': 'Аккаунт не обладает привелегиями модератора'})
        except:
            return Response({'err': 'Вы не авторизированы'})




class ModerPPUList(ListAPIView):
    serializer_class = ModerPPUSerializer

    def get_queryset(self):
        try:
            moder = Acc.objects.get(username=request.query_params.get('username'))
        except:
            return {'err': "Аккаунт с этим именем уже занят"}

        
        if moder.is_moder:
            queryset = PPU.objects.filter(moder=moder)
            return queryset
        else:
            return {'err': "Аккаунт не обладает привелегиями модератора"}




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def moder_list_ppus(request):
    token = request.headers.get('Authorization').split(' ')[1]
    info = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    
    username = request.query_params['username']
    try:
        acc = Acc.objects.get(username=info.get('username'))
        if acc.is_moder:
            try:
                moder = Acc.objects.get(username=username)

                ppus = []
                if moder.is_moder:
                    ppus1 = PPU.objects.filter(moder=moder, status=1)
                    ppus2 = PPU.objects.filter(moder=moder, status=2)
                    ppus = ppus1 | ppus2
                    ppus = serializers.serialize('json', ppus)
                    print(ppus)
                    ppus = json.loads(ppus)
                    return Response(ppus)
                else:
                    return Response({'err': "Аккаунт не обладает привелегиями модератора"})
            except:
                return Response({"err": "Аккаунт с данным именем не найден"})
        else:
            return Response({'err': "Вы не обладаете правами модератора"})
    except:
        return Response({'err': "Аккаунт с этим именем не найден"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def moder_answer(request):
    data = request.data
    ppu = PPU.objects.get(title=data.get('title'))
    
    token = request.headers.get('Authorization').split(' ')[1]
    info = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    
    try:
        acc = Acc.objects.get(username=info.get('username'))
        ppu = PPU.objects.get(title=data.get('title'))
        if acc.is_moder and ppu in acc.get_moder_ppus():
            if data.get('action') == 'confirm':
                ppu.status = '5'
                deadline = data.get('deadline')
                    #22/10/2004 12:21
                    #deadline = datetime.datetime.strptime(deadline, '%d/%m/%Y %H:%M')
                    
                ppu.deadlines = deadline
                    
                ppu.vned = Acc.objects.get(username=data.get('vned'))
                ppu.save()
                return Response("ППУ отправлено на внедрение")

            elif data.get('action') == 'update':
                ppu.status = '4'
                ppu.save()
                return Response('ппу отправлено на доработку')

            elif data.get('action') == 'denied':
                ppu.status = '7'
                ppu.save()
                return Response("ппу отказано")

            elif data.get('action') == 'next_check':
                if ppu.status == '1':
                    try:
                        ppu.status = '2'
                        moder = data.get('moder')
                        ppu.moder = Acc.objects.get(username=moder)
                        ppu.save()
                        return Response('ппу отправлено на рассмотрение другому модератору')
                    except:
                        return Response({'err': "Модератор с указанным ником не найден"})
                elif ppu.status == '2':
                    moder = data.get('moder')
                    ppu.status = '3'
                    ppu.moder = ""
                        
                    ppu.save()
                    return Response("ппу отправлено на доработку экспертной группе")

                else:
                    return Response({'err': "Данное ППУ больше не рассматривается"})
            else:
                return Response({'err': 'действие введено не правильно или не указано'})

            return Response('a')
        else:
            return Response({'err': 'Вы не обладаете правами модератора, либо данное ППУ рассматривается не вами'})
    except:
        return Response({'err': "Вы не авторизованы"})


"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def moder_select_vned(request):
    data = request.data
    ppu = PPU.obejcts.get(title=data.get('title'))
    try:
        vned = Acc.objects.get(username=data.get('ispoln'))
    except:
        return Request('Нет аккаунта с этим именем')    

    if not vned.is_vned:
        return Request('Пользователь не является ответственным за внедрение ППУ')




def moder_list_ppus(request, username):
    try:
        moder = Acc.objects.get(username=moder_username)
    except:
        return Response({'err': "account with this name does not found"})

    ppus = []
    if moder.is_moder:
        ppus = PPU.objects.filter(moder=moder)
        ppus = serializers.serialize('json', ppus)
        return JsonResponse(ppus)
    else:
        return JsonResponse({'err': "this acc is not moder"})




class ListCheckingPPUs(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PPUSerializer
    model = PPU
    queryset = PPU.objects.filter(status=1)


    def get(self, request):
        try:
            request.data['status']
            status = request.data['status']
        except:
            status = 1

        try:
            request.data['moder']
            try:
                acc = Acc.objects.get(username=request.data['moder'])
                    
                ppus = PPU.objects.filter(status=status, author=acc)
                serializer = PPUSerializer(ppus)
            except:
                return Response('moder with this username does not exists')
        except:
            ppus = PPU.objects.filter(status=status)
            serializer = PPUSerializer(ppus)
        print(dir(ppus))
        return Response(serializer)

class ModerListPPUS(APIView):
    parser_classes = (JSONParser, )

    def get(request, moder_username):
        print(moder_username)
        try:
            moder = Acc.objects.get(username=moder_username)
        except:
            return Response({'err': "account with this name does not found"})

        ppus = []
        if moder.is_moder:
            ppus = PPU.objects.filter(moder=moder)
            
            return Response(ppus)
        else:
            return Response({'err': "this acc is not moder"})        



"""