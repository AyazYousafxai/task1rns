from rest_framework import serializers
from rns_store.models import Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = (
            "name",
            "description",
            "logo",
            "tags",
            "likes",
        )
