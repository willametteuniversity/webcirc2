from django.forms import widgets
from rest_framework import serializers
from website.models import Collection

class CollectionSerializer(serializers.Serializer):
    CollectionID = serializers.Field()
    CollectionName = serializers.Field()
    CollectionDescription = serializers.Field()

    def restore_object(self, attrs, instance=None):
        '''
        Create or update a new Collection instance, given a dictionary of deserialized field values.
        '''
        # If we have an already existing instance (that is, we're updating a Collection), this if
        # is triggered.
        if instance:
            # attrs is a dictionary containing our JSON data. We use get() to access a particular
            # attribute in attrs and assign it to the instance. The second argument is a default
            # which means we default to the current value.
            instance.CollectionName = attrs.get('CollectionName', instance.CollectionName)
            instance.CollectionDescription = attrs.get('CollectionDescription', instance.CollectionDescription)
            return instance

        # If we didn't use an already existing instance, create a new one and use Python's
        # keyword expansion.
        return Collection(**attrs)
        # This is really:
        # Collection(CollectionName=attrs['CollectionName'], CollectionDescription=attrs['CollectionDescription'])
