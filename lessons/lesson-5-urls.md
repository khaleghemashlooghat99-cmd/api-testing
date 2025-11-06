# Lesson 5: URL Routing

## Learning Goals
- Understand DRF routers and automatic URL generation
- Learn how to connect ViewSets to URLs
- Configure main project URL routing
- Set up authentication endpoints
- Understand URL patterns and API structure

## URL Routing in Django and DRF

### What is URL Routing?
URL routing maps web addresses (URLs) to specific views or ViewSets. In DRF, routing connects HTTP requests to the appropriate ViewSet methods.

### Traditional Django URLs
```python
# Traditional approach - manual URL definitions
urlpatterns = [
    path('api/contacts/', views.contact_list, name='contact-list'),
    path('api/contacts/<int:pk>/', views.contact_detail, name='contact-detail'),
    # Need to define each URL pattern manually
]
```

### DRF Router Approach
```python
# DRF approach - automatic URL generation
router = DefaultRouter()
router.register(r'contacts', ContactViewSet)
# Creates all CRUD URLs automatically
```

## DRF Routers

### DefaultRouter
The `DefaultRouter` is the most commonly used router in DRF:

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')
```

### What DefaultRouter Provides
1. **List endpoint**: GET /api/contacts/
2. **Create endpoint**: POST /api/contacts/
3. **Detail endpoint**: GET /api/contacts/{id}/
4. **Update endpoint**: PUT /api/contacts/{id}/
5. **Partial update endpoint**: PATCH /api/contacts/{id}/
6. **Delete endpoint**: DELETE /api/contacts/{id}/
7. **Browsable API interface**: HTML interface for testing

### Router Registration Parameters
```python
router.register(prefix, viewset, basename=None)
```

- **prefix**: URL prefix (e.g., 'contacts' → /api/contacts/)
- **viewset**: ViewSet class to register
- **basename**: Base name for URL names (optional, usually auto-generated)

## Our App URL Configuration

### contacts/urls.py
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
```

### What This Creates
The router automatically creates these URL patterns:

```
GET    /api/contacts/          → ContactViewSet.list()
POST   /api/contacts/          → ContactViewSet.create()
GET    /api/contacts/{id}/     → ContactViewSet.retrieve()
PUT    /api/contacts/{id}/     → ContactViewSet.update()
PATCH  /api/contacts/{id}/     → ContactViewSet.partial_update()
DELETE /api/contacts/{id}/     → ContactViewSet.destroy()
```

## Main Project URL Configuration

### api_project/urls.py
```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    # API endpoints
    path('api/', include('contacts.urls')),
    # DRF authentication endpoints
    path('api-auth/', include('rest_framework.urls')),
    # Token authentication endpoint
    path('api-token/', obtain_auth_token),
]
```

### URL Pattern Breakdown

#### Admin Interface
```python
path('admin/', admin.site.urls)
```
- URL: `/admin/`
- Purpose: Django admin interface
- Usage: Data management and testing

#### Main API Endpoints
```python
path('api/', include('contacts.urls'))
```
- URL: `/api/contacts/`
- Purpose: Main contact CRUD endpoints
- All contact operations

#### DRF Authentication
```python
path('api-auth/', include('rest_framework.urls'))
```
- URL: `/api-auth/login/`
- Purpose: DRF browsable API login
- Usage: Logging into the HTML API interface

#### Token Authentication
```python
path('api-token/', obtain_auth_token)
```
- URL: `/api-token/`
- Purpose: Get authentication token
- Usage: API clients to get auth tokens

## Authentication Endpoints

### Token Authentication Endpoint
```python
from rest_framework.authtoken.views import obtain_auth_token
path('api-token/', obtain_auth_token)
```

#### How to Use
```bash
# Request
POST /api-token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}

# Response
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

#### Using the Token
```bash
# In subsequent requests
GET /api/contacts/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### DRF Browsable API Authentication
```python
path('api-auth/', include('rest_framework.urls'))
```

#### What This Provides
- Login/logout forms for the browsable API
- Session-based authentication for browser testing
- Easy way to test APIs without external tools

## URL Patterns and Naming

### Automatic URL Names
DRF router automatically generates URL names:

```python
# basename='contact' generates:
name='contact-list'    # /api/contacts/
name='contact-detail'   # /api/contacts/{id}/

# Used in templates and reverse URL resolution
{% url 'contact-list' %}
{% url 'contact-detail' pk=1 %}
```

### Custom URL Names
```python
router.register(r'contacts', ContactViewSet, basename='contact')
```

- **basename**: Required when using viewsets with `queryset` attribute
- **Purpose**: Generates consistent URL names
- **Usage**: Template linking and reverse URL resolution

## Testing URL Configuration

### Django Shell URL Testing
```bash
python manage.py shell
```

```python
from django.urls import reverse
from rest_framework.test import APIRequestFactory

# Test URL resolution
print(reverse('contact-list'))     # /api/contacts/
print(reverse('contact-detail', kwargs={'pk': 1}))  # /api/contacts/1/

# Test URL patterns
from django.urls import resolve
resolver = resolve('/api/contacts/')
print(resolver.func)  # ViewSet function
print(resolver.kwargs)  # URL parameters
```

### Testing with curl
```bash
# Test that API endpoints exist
curl -I http://localhost:8000/api/contacts/
# Should return 401 Unauthorized (requires authentication)

# Test token endpoint
curl -I http://localhost:8000/api-token/
# Should return 405 Method Not Allowed (needs POST)
```

## URL Configuration Best Practices

### URL Structure Guidelines
```python
# Good - consistent and clear
path('api/', include('contacts.urls'))
path('api/', include('users.urls'))

# Bad - inconsistent
path('contacts/', include('contacts.urls'))
path('users/', include('users.urls'))
```

### API Versioning Preparation
```python
# Prepare for future API versions
path('api/v1/', include('contacts.urls'))

# Later you can add v2 without breaking v1
path('api/v1/', include('contacts.urls'))
path('api/v2/', include('contacts.urls'))
```

### Multiple Apps URL Organization
```python
# Main project urls.py
urlpatterns = [
    path('api/', include('contacts.urls')),
    path('api/', include('users.urls')),
    path('api/', include('notifications.urls')),
]

# contacts/urls.py
router.register(r'contacts', ContactViewSet)

# users/urls.py
router.register(r'users', UserViewSet)
# Result: /api/contacts/, /api/users/
```

## Troubleshooting URL Issues

### Common URL Problems

#### 404 Not Found
```python
# Check if URL pattern exists
# Verify include paths are correct
# Check prefix in router.register()
```

#### 405 Method Not Allowed
```python
# Check if ViewSet supports the HTTP method
# Verify router configuration
# Check if method is allowed in ViewSet
```

#### Reverse URL Not Found
```python
# Check if basename is specified
# Verify viewset registration
# Check for naming conflicts
```

### Debugging Tools

#### Django URL Debug
```bash
# Show all URL patterns
python manage.py show_urls

# Or use Django shell
from django.urls import get_resolver
from django.urls.resolvers import URLResolver, URLPattern

def show_urls(urllist, depth=0):
    for entry in urllist:
        if isinstance(entry, URLResolver):
            show_urls(entry.url_patterns, depth + 1)
        elif isinstance(entry, URLPattern):
            indent = "  " * depth
            print(f"{indent}{entry.pattern} -> {entry.callback}")

resolver = get_resolver()
show_urls(resolver.url_patterns)
```

#### DRF Browsable API
- Visit `/api/contacts/` in browser
- Check if browsable API loads
- Look at generated URLs and forms

## Advanced URL Configuration

### Multiple Routers
```python
# contacts/urls.py
contact_router = DefaultRouter()
contact_router.register(r'contacts', ContactViewSet)

# users/urls.py
user_router = DefaultRouter()
user_router.register(r'users', UserViewSet)

# Main urls.py
urlpatterns = [
    path('api/', include(contact_router.urls)),
    path('api/', include(user_router.urls)),
]
```

### Nested URLs
```python
# For nested resources like /api/users/{user_id}/contacts/
router = DefaultRouter()
router.register(r'users', UserViewSet)

# In UserViewSet, add custom actions
@action(detail=True, methods=['get'])
def contacts(self, request, pk=None):
    # Logic for user's contacts
    pass
```

### Custom URL Patterns
```python
# Adding custom endpoints alongside ViewSet URLs
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/contacts/export/', views.export_contacts),
    path('api/contacts/import/', views.import_contacts),
]
```

## Key Concepts Covered

### DRF Routers
- **DefaultRouter**: Automatic CRUD URL generation
- **URL registration**: Connect ViewSets to URL patterns
- **Browsable API**: HTML interface for testing

### URL Configuration
- **Project URLs**: Main URL configuration file
- **App URLs**: App-specific URL patterns
- **Include patterns**: Organize URLs by app

### Authentication Endpoints
- **Token authentication**: Get API tokens
- **Browsable API login**: Browser-based testing
- **Session vs Token**: Different authentication methods

### URL Organization
- **Consistent patterns**: Clear API structure
- **Version preparation**: Future API versioning
- **Multiple apps**: Complex application organization

## Success Criteria
- [ ] All API endpoints are accessible
- [ ] URL patterns follow REST conventions
- [ ] Authentication endpoints work correctly
- [ ] Browsable API is accessible
- [ ] No 404 or 405 errors for valid endpoints

## Common Issues and Solutions

### URL Not Found (404)
- Check URL pattern registration
- Verify include paths
- Check prefix in router.register()

### Method Not Allowed (405)
- Verify ViewSet supports the HTTP method
- Check permission classes
- Verify authentication requirements

### Authentication Issues
- Check token endpoint configuration
- Verify DRF settings
- Check permission class configuration

## Next Steps
In the next lesson, we'll set up authentication and test the complete authentication flow.

## Additional Resources
- [Django URL Dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)
- [DRF Routers Documentation](https://www.django-rest-framework.org/api-guide/routers/)
- [DRF Authentication](https://www.django-rest-framework.org/api-guide/authentication/)