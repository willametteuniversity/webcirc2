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
