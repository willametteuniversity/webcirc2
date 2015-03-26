from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *
from rest_framework import status
from django.http import HttpResponse

import datetime
@api_view(['Get'])
def reservationActions(request, pk):
    try:
        return Response(ActionSerializer(Reservation.objects.get(ReservationID=pk).action_set.all(), many=True).data, status=200)
    except Reservation.DoesNotExist:
        return Response(status=404)


@api_view(['POST'])
def addActionToReservation(request, pk):
    try:
        action = Action.objects.get(pk=pk)
        reservation = Reservation.objects.get(pk=request.POST['reservation'])
    except (Action.DoesNotExist, Reservation.DoesNotExist):
        return Response(status=404)
    try:
        reservation.action_set.add(action)
    except:
        return Response(status=500)
    return Response(status=201)


@api_view(['POST'])
def removeActionFromReservation(request, pk):
    try:
        action = Action.objects.get(pk=pk)
        reservation = Reservation.objects.get(pk=request.POST['reservation'])
    except (Action.DoesNotExist, Reservation.DoesNotExist):
        return Response(status=404)
    try:
        reservation.action_set.remove(action)
    except:
        return Response(status=500)
    return Response(status=200)


@api_view(['Get', 'POST'])
def actionList(request, date=None):
    if request.method == u'GET':
        actions = Action.objects.all()
        if date != None:
            today = datetime.datetime.strptime(date, '%Y-%m-%d')
            actions = actions.filter(StartTime__year=today.year,
                                     StartTime__month=today.month,
                                     StartTime__day=today.day)

        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = ActionSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print serializer.errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def actionDetail(request, pk):
    try:
        action = Action.objects.get(ActionID=pk)
    except Action.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == u'GET':
        serializer = ActionSerializer(action)
        return Response(serializer.data)
    elif request.method == u'PUT':
        serializer = ActionSerializer(action, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == u'DELETE':
        action.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
