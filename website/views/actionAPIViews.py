from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *
from rest_framework import status
from django.http import HttpResponse


@api_view(['Get'])
def reservationActions(request, pk):
    try:
        return Response(ActionSerializer(Reservation.objects.get(ReservationID=pk).action_set.all(), many=True).data, status=200)
    except Reservation.DoesNotExist:
        return Response(status=404)


@api_view(['Get', 'POST'])
def actionList(request):
    if request.method == u'GET':
        actions = Action.objects.all()
        serializer = ActionSerializer(actions, many=True)
        return Response(serializer.data)
    elif request.method == u'POST':
        serializer = ActionSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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