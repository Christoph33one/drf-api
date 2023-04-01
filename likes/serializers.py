from django.db import IntegrityError
from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model
    The create method handles the unique constraint on 'owner' and 'post'
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        # stops the user from liking the same post twice
        fields = [
            'id', 'created_at', 'owner', 'post'
        ]

    # how to prvent out API users from liking a post twice!
    def create(self, validated_data):
        # this stops the server crashing and gives a IntegrityError
        # 'detail': 'possible duplicate' - user is liking the same post twice!
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })

