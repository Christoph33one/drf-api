from rest_framework import serializers
from .models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.porfile.image.url')
    id = serializers.SerializerMethodField()

    # validates an image each time it is uploaded or a post is created!
    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2: # this give a MB size limit for all images
            # raise errors - image to big in MB
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
            # raise error if image width is bigger than 4096px
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px'
            )
            # raise error if inmage height is bigger than 4096px
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger that 4096px'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

# Adding a like Id field to all posts. ß
    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'content', 'image', 'image_filter',
            'like_id'
        ]
