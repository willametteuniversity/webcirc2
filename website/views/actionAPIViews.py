from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *

@api_view(['Get'])
def reservationActions(request, pk):
    return Response(ActionSerializer(Reservation.objects.get(pk=pk).action_set.all(), many=True).data, status=200)

@api_view(['Get'])
def actionList():
    pass


@api_view(['POST', 'PUT', 'DELETE'])
def actionDetail():
    pass