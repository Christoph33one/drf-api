from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from followers.model import Follower
from followers.serializers import FollowerSerializer


class FollowerList(generics.ListCreateAPIView):
    serializer_class = FollowerSerializer()
    queryset = Follower.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()


"""Overall, these views allow users to create,
retrieve, update, and delete Follower instances
via HTTP requests, while enforcing appropriate permissions
and serialization/deserialization using the FollowerSerializer.
"""
