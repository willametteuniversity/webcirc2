from django.forms import widgets
from rest_framework import serializers
from website.models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
            model = Collection
