# Lesson 4: DRF Views and ViewSets

## Learning Goals
- Understand the difference between traditional views and ViewSets
- Learn how ViewSets automatically provide CRUD operations
- Create custom permission classes
- Understand queryset filtering for user-specific data
- Learn how to automatically set object ownership

## What are DRF Views?

**Views** handle HTTP requests and return HTTP responses. In DRF, views are responsible for:
- Processing incoming requests
- Applying business logic
- Serializing data for responses
- Handling errors and validation

## Traditional Views vs ViewSets

### Traditional API Views
```python
# Traditional approach - requires multiple views
class ContactList(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
```

### ViewSet Approach
```python
# ViewSet approach - single class for all CRUD operations
class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    # Automatic CRUD: list, create, retrieve, update, destroy
```

## Why Use ViewSets?

### Benefits of ViewSets
- **Less code**: One class instead of multiple views
- **Automatic CRUD**: Built-in list, create, retrieve, update, destroy
- **Consistent URLs**: DRF router creates all URL patterns
- **Convention over configuration**: Standardized patterns

### When to Use ViewSets
- Standard CRUD operations
- RESTful API design
- Model-based resources
- When you want all HTTP methods supported

### When NOT to Use ViewSets
- Non-standard HTTP operations
- Custom business logic per endpoint
- When you need fine-grained control

## Our ContactViewSet Analysis

```python
from rest_framework import viewsets, permissions
from .models import Contact
from .serializers import ContactSerializer

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

## Automatic CRUD Operations

### What ModelViewSet Provides
| HTTP Method | Action | ViewSet Method | Description |
|-------------|--------|----------------|-------------|
| GET | List | `.list()` | Get all objects |
| POST | Create | `.create()` | Create new object |
| GET | Retrieve | `.retrieve()` | Get single object |
| PUT/PATCH | Update | `.update()` | Update object |
| DELETE | Destroy | `.destroy()` | Delete object |

### URL Mapping
```
GET    /api/contacts/        → list all contacts
POST   /api/contacts/        → create new contact
GET    /api/contacts/1/      → get contact with id=1
PUT    /api/contacts/1/      → update contact with id=1
PATCH  /api/contacts/1/      → partial update contact with id=1
DELETE /api/contacts/1/      → delete contact with id=1
```

## Permission Classes

### Why Permissions Matter
- **Security**: Control who can access what
- **Data isolation**: Users can't see each other's data
- **API design**: Define access rules per endpoint

### Built-in Permission Classes
```python
from rest_framework import permissions

# Common permission classes
permissions.AllowAny          # Anyone can access
permissions.IsAuthenticated   # Must be logged in
permissions.IsAdminUser       # Must be admin
permissions.IsAuthenticatedOrReadOnly
```

### Our Permission Configuration
```python
permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
```
- **IsAuthenticated**: User must be logged in
- **IsOwnerOrReadOnly**: Can read any, but only edit own objects

## Custom Permission Classes

### Our IsOwnerOrReadOnly Permission
```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for object owner
        return obj.owner == request.user
```

### Understanding SAFE_METHODS
```python
permissions.SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
```
- **GET**: Read operation
- **HEAD**: Get headers only
- **OPTIONS**: Get allowed HTTP methods
- **Unsafe methods**: POST, PUT, PATCH, DELETE

### Custom Permission Logic
```python
class IsOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user  # Only owner can do anything

class CanEditOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow staff to edit any object
        return obj.owner == request.user or request.user.is_staff
```

## Queryset Filtering

### Why Filter QuerySets?
- **Data isolation**: Users should only see their own data
- **Performance**: Only query necessary data
- **Security**: Prevent unauthorized data access

### Our get_queryset Method
```python
def get_queryset(self):
    return Contact.objects.filter(owner=self.request.user)
```

### What This Does
- **Filters by owner**: Only contacts belonging to current user
- **Automatic filtering**: Applied to all operations (list, retrieve, etc.)
- **Security**: Users can't access other users' contacts

### Advanced Queryset Filtering
```python
def get_queryset(self):
    queryset = Contact.objects.filter(owner=self.request.user)

    # Filter by name if provided in query params
    name_filter = self.request.query_params.get('name')
    if name_filter:
        queryset = queryset.filter(name__icontains=name_filter)

    # Filter by email if provided
    email_filter = self.request.query_params.get('email')
    if email_filter:
        queryset = queryset.filter(email__icontains=email_filter)

    return queryset
```

## perform_create for Automatic Ownership

### Why Override perform_create?
- **Automatic ownership**: Set owner without requiring in request
- **Security**: Users can't assign contacts to other users
- **Convenience**: Cleaner API (don't need to send owner ID)

### Our perform_create Method
```python
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
```

### What This Does
- **Automatically sets owner**: Uses authenticated user
- **Happens during creation**: Before database save
- **Transparent to client**: Owner field not required in request

### Alternative Approaches
```python
# Using default value in model
# models.py
owner = models.ForeignKey(User, on_delete=models.CASCADE, default=lambda: None)

# In serializer
# serializers.py
def create(self, validated_data):
    validated_data['owner'] = self.context['request'].user
    return super().create(validated_data)
```

## Testing ViewSets

### Django Shell Testing
```bash
python manage.py shell
```

```python
from contacts.models import Contact
from contacts.serializers import ContactSerializer
from contacts.views import ContactViewSet
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

# Create test data
user = User.objects.create_user('testuser', 'test@example.com', 'password')
contact = Contact.objects.create(owner=user, name='Test Contact', email='test@example.com')

# Create a mock request
factory = APIRequestFactory()
request = factory.get('/api/contacts/')
request.user = user

# Test the ViewSet
viewset = ContactViewSet()
viewset.request = request
viewset.format_kwarg = None

# Test get_queryset
queryset = viewset.get_queryset()
print(f"Contacts found: {queryset.count()}")  # Should be 1
print(f"User's contacts: {[c.name for c in queryset]}")
```

### Understanding ViewSet Context
```python
def get_serializer_context(self):
    context = super().get_serializer_context()
    context['request'] = self.request
    return context
```
- **Request context**: Available in serializer for validation
- **User access**: Can access authenticated user
- **Custom data**: Add additional context as needed

## Common ViewSet Patterns

### Search and Filtering
```python
class ContactViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Contact.objects.filter(owner=self.request.user)

        # Search by name or email
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(email__icontains=search)
            )

        return queryset
```

### Ordering
```python
class ContactViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Contact.objects.filter(owner=self.request.user)

        # Ordering by name or created_at
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
```

### Custom Actions
```python
class ContactViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def mark_favorite(self, request, pk=None):
        contact = self.get_object()
        contact.is_favorite = True
        contact.save()
        return Response({'status': 'marked as favorite'})

    @action(detail=False, methods=['get'])
    def favorites(self, request):
        favorites = Contact.objects.filter(
            owner=request.user,
            is_favorite=True
        )
        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)
```

## Key Concepts Covered

### ViewSet Architecture
- **ModelViewSet**: Full CRUD operations in one class
- **Automatic URL routing**: DRF router creates all endpoints
- **Convention over configuration**: Standardized patterns

### Permission System
- **Multiple permission classes**: Applied in order
- **Object-level permissions**: Control access to specific objects
- **Custom permissions**: Implement business logic

### Queryset Management
- **User filtering**: Ensure data isolation
- **Performance**: Query only necessary data
- **Security**: Prevent unauthorized access

### Automatic Ownership
- **perform_create**: Set object owner automatically
- **Security**: Users can't assign to other users
- **API design**: Cleaner request/response

## Success Criteria
- [ ] ContactViewSet created with all CRUD operations
- [ ] Users can only see their own contacts
- [ ] Ownership is automatically set on creation
- [ ] Permissions work correctly
- [ ] API endpoints respond appropriately

## Common Issues

### Permission Problems
1. **Users can see other users' data**: Check get_queryset method
2. **401 Unauthorized**: User not authenticated
3. **403 Forbidden**: Permission denied (check permission_classes)

### Queryset Issues
1. **No data returned**: Check filtering logic
2. **Performance problems**: Optimize queryset
3. **Data leakage**: Ensure proper user filtering

## Next Steps
In the next lesson, we'll set up URL routing to connect our ViewSets to actual API endpoints.

## Additional Resources
- [DRF ViewSets Documentation](https://www.django-rest-framework.org/api-guide/viewsets/)
- [DRF Permissions Documentation](https://www.django-rest-framework.org/api-guide/permissions/)
- [DRF Routers Documentation](https://www.django-rest-framework.org/api-guide/routers/)