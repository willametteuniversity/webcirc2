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

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation


class ActionStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionState


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


class ItemHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemHistory


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action