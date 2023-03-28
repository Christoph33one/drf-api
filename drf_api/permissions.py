from rest_framework import permissions


# giving custom permissions to the DetailView. not form will show if user is logged out .
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # check if the user is accessing read only content. Return true
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
        # else return true only if the user making the request owns the profile.
