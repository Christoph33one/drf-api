from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class PostList(APIView):
    serializer_class = PostSerializer
    # creates a user must be logged in for add a post (show form in API!)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class PostDetail(APIView):
    # permission_classes = only owner can edit or delete the post
    permission_classes = [IsOwnerOrReadOnly]
    # renders the edit post form in the browser
    serializer_class = PostSerializer

    # get object  method
    def get_object(self, pk):
        # try to get a post by pk
        try:
            post = Post.objects.get(pk=pk)
            # ask for permission to edit and then return the updated post
            self.check_object_permissions(self.request, post)
            return post
        # if post dose not exist, raise 404
        except Post.DoesNotExist:
            raise Http404

    # retiieve a post by Id method
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, context={'request': request}
        )
        # return serializer data in the Response
        return Response(serializer.data)

    # put method to update (edit posts)
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, data=request.data, context={'request': request}
            )
        # if updated data is vaild then save data and return data and update the responce
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # detele a post method
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        # once post is deleted, a 204 no content message will so in API
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
