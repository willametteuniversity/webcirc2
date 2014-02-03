from django.forms import widgets
from rest_framework import serializers
from website.models import Collection
from website.models import Label

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