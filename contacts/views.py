from rest_framework import viewsets, permissions
from .models import Contact
from .serializers import ContactSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read-only access is allowed for any request.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the contact.
        return obj.owner == request.user

class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Contact model providing full CRUD operations.
    - List all contacts for the authenticated user
    - Create a new contact
    - Retrieve, update, or delete a specific contact
    - Enforces user isolation (users can only see their own contacts)
    - Includes object-level permissions for write operations
    """
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Override get_queryset to filter contacts by the current user.
        This ensures users can only see their own contacts.
        """
        return Contact.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Override perform_create to automatically set the owner
        to the current authenticated user.
        """
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        """
        Add additional context to the serializer.
        This can be useful for custom validation or field computation.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
