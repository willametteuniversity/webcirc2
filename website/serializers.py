from django.forms import widgets
from rest_framework import serializers
from website.models import *


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label


class LabelNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabelNotes


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem


class NonInventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonInventoryItem


class ConsumableItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumableItem


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation


class ReservationActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationAction


class ItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModel


class ItemBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemBrand


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building


class ActionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionType


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile


class ReservationDetailSerializer(serializers.ModelSerializer):
    reservation = None
    all_actions = []
    all_reservation_actions = []

    def restore_objects(self, dictionary, reservation=None):
        # TODO: Where do I need to check for many?  if many, dictionary is list of dictionaries?
        if reservation is None:
            self.reservation = Reservation(dictionary)
        else:
            self.reservation = reservation
            self.reservation.__dict__ = dictionary
        for action in dictionary[u'actions']:            # dictionary["actions"] is a list of dictionaries
            current_action = Action(action)
            self.all_actions.append(current_action)
            self.all_reservation_actions.append(ReservationAction(self.reservation, current_action))

    def is_valid(self):
        pass

    def save(self):
        self.reservation.save()
        for action in self.all_actions:
            action.save()
        for reservation_action in self.all_reservation_actions:
            reservation_action.save()

    def data(self, reservation):
        reservation_actions = ReservationAction.objects.all()
        reservation_dictionary = {}
        for reservation_action in reservation_actions:
            if reservation_action[u'Reservation'] is reservation:
                reservation_dictionary.update(reservation_action[u'Action'])
        # return the dictionary, turned into json.