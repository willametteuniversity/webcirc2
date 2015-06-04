from rest_framework.decorators import api_view
from rest_framework.response import Response
from website.serializers import *
from django.http import HttpResponse


@api_view(['GET'])
def reservationSearch(request, username=None, em=None, start_date=None, end_date=None):
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
        pass
        ## TODO: filter query set by date
    return Response(ReservationSerializer(Reservation.objects.all(), many=True).data, status=200)


@api_view(['GET'])
def reservationOwnerSearch(request, username=None, em=None, start_date=None, end_date=None):
    query = None
    owner = None
    try:
        if username is not None:
            owner = User.objects.get(username=username)  # Lookup pk of user, filter by OwnerID
        elif em is not None and owner is None:
            owner = User.objects.get(email=em)
    except User.DoesNotExist:
        return Response(status=404)
    if username is not None:
        query = Reservation.objects.filter(OwnerID=owner)
    if em is not None:
        query = Reservation.objects.filter(em=em)
    if query is None:
        return Response(status=404)
    if (start_date is not None) and (end_date is not None):
        pass
        ## TODO: filter query set by date
    return Response(ReservationSerializer(query, many=True).data, status=200)


@api_view(['GET', 'POST'])
def reservationList(request):
    if request.method == u'GET':
        return Response(ReservationSerializer(Reservation.objects.all(), many=True).data)
    elif request.method == u'POST':
        serializer = ReservationSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=404)


@api_view(['GET', 'PUT', 'DELETE'])
def reservationDetail(request, pk):
    try:
        reservation = Reservation.objects.get(ReservationID=pk)
    except Reservation.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == u'GET':
        return Response(ReservationSerializer(reservation).data)
    elif request.method == u'PUT':
        serializer = ReservationSerializer(reservation, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == u'DELETE':
        reservation.delete()
        return HttpResponse(status=204)
