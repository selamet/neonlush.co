from rest_framework import serializers

from neonlush.apps.main.models import NotifyMe


class NotifyMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotifyMe
        fields = ('email', 'created_at')
        extra_kwargs = {
            'created_at': {'read_only': True},
        }
