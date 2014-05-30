from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *


@api_view(['GET'])
def reservationLookup(request, pk=None, username=None, em=None, start_date=None, end_date=None):
    if pk is not None:
        try:
            reservation = Reservation.objects.get(ReservationID=pk)
            return Response(ReservationSerializer(reservation).data, status=200)
        except Reservation.DoesNotExist:
            return Response(status=404)
    if em is not None:
        try:
            return Response(ReservationSerializer(Reservation.objects.filter(CustomerEmail=em), many=True).data, status=200)
        except Reservation.DoesNotExist:
            return Response(status=404)
    if username is not None:
        try:
            user_id = User.objects.get(username=username)
            return Response(ReservationSerializer(Reservation.objects.filter(CustomerID=user_id), many=True).data, status=200)
        except User.DoesNotExist:
            return Response(status=404)
    if (start_date is not None) and (end_date is not None):
        pass    # return filtered by dates
    return Response(ReservationSerializer(Reservation.objects.all(),many=True).data, status=200)


@api_view(['GET'])
def reservationOwnerLookup(request, username=None, em=None, start_date=None, end_date=None):
    query = None
    if username is not None:
        pass    # define query as a new query set filtered by username
    if em is not None:
        pass    # define query as a new query set filtered by email
    if query is None:
        return Response(status=404)
    if (start_date is not None) and (end_date is not None):
        pass    # further filter query by the start and end dates
    # return query


@api_view(['POST', 'PUT', 'DELETE'])
def reservationManage(request, pk=None, em=None, fn=None, n=None):
    # TODO: Check the current user's permissions, ensure they can use reservationManage
    if request.method == u'POST':
        pass    # create a new reservation
        # decode the json into a dictionary
        # pass that into the serializer
        # if valid, have serialzer save each
    elif request.method == u'PUT':
        pass    # update the reservation with pk
    elif request.method == u'DELETE':
        pass    # delete the reservation with pk
