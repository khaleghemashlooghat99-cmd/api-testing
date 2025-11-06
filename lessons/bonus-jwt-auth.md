# Bonus Lesson: JWT Authentication

## Learning Goals
- Understand JWT (JSON Web Tokens) vs Token authentication
- Learn JWT structure and benefits
- Implement JWT authentication in Django REST Framework
- Understand token refresh patterns
- Learn when to use JWT vs Token authentication
- Configure JWT for production use

## What is JWT?

**JWT (JSON Web Token)** is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object.

### JWT vs Traditional Token Authentication

#### Traditional Token Authentication (Django's built-in)
- **Database lookup**: Token stored in database
- **Server state**: Requires database hit for validation
- **Simple**: Easy to implement and understand
- **Instant revocation**: Can delete token from database

#### JWT Authentication
- **Stateless**: No database lookup for validation
- **Self-contained**: Token contains user information
- **Scalable**: Works well across multiple servers
- **Expires**: Tokens have built-in expiration

## JWT Structure

A JWT consists of three parts separated by dots (`.`):

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### 1. Header (Algorithm & Token Type)
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### 2. Payload (Claims)
```json
{
  "user_id": 1,
  "username": "johndoe",
  "exp": 1516239022,
  "iat": 1516239022,
  "jti": "unique-token-id"
}
```

### 3. Signature (Verification)
```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  your-256-bit-secret
)
```

## Installing JWT Support

### Simple JWT Package
We already included `djangorestframework-simplejwt` in our requirements:

```
djangorestframework-simplejwt==5.3.0
```

### JWT Configuration
Add JWT to your Django settings:

```python
# api_project/settings.py

INSTALLED_APPS = [
    # ... other apps
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # Keep token authentication for compatibility
        'rest_framework.authentication.TokenAuthentication',
        # Add JWT authentication
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# JWT Configuration
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}
```

## JWT URL Configuration

### Add JWT Endpoints
Update your main URL configuration:

```python
# api_project/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # API endpoints
    path('api/', include('contacts.urls')),
    # DRF authentication endpoints
    path('api-auth/', include('rest_framework.urls')),
    # Traditional token authentication
    path('api-token/', obtain_auth_token),

    # JWT Authentication endpoints
    path('api/jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
```

## JWT Authentication Flow

### 1. Obtain JWT Token Pair
```bash
curl -X POST http://localhost:8000/api/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2. Use Access Token for API Requests
```bash
curl -X GET http://localhost:8000/api/contacts/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

### 3. Refresh Access Token
When access token expires (after 5 minutes in our config):

```bash
curl -X POST http://localhost:8000/api/jwt/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."  // New refresh token if ROTATE_REFRESH_TOKENS=True
}
```

### 4. Verify Token (Optional)
```bash
curl -X POST http://localhost:8000/api/jwt/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

**Success Response:**
```json
{}
```

**Error Response:**
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

## Custom JWT Payload

### Custom Claims
You can add custom data to JWT tokens:

```python
# contacts/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom response data
        data['user_id'] = self.user.id
        data['username'] = self.user.username

        return data

# Custom token view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Add additional user data to response
        if response.status_code == 200:
            user = self.user
            response.data.update({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_staff': user.is_staff,
                }
            })

        return response
```

### Update URLs to use custom view
```python
# api_project/urls.py
from contacts.views import CustomTokenObtainPairView

urlpatterns = [
    # ... other urls
    path('api/jwt/create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # ... other jwt urls
]
```

## Testing JWT Authentication

### Complete JWT Workflow Test

```bash
# 1. Get JWT token pair
JWT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}')

ACCESS_TOKEN=$(echo $JWT_RESPONSE | jq -r .access)
REFRESH_TOKEN=$(echo $JWT_RESPONSE | jq -r .refresh)

echo "Access Token: $ACCESS_TOKEN"
echo "Refresh Token: $REFRESH_TOKEN"

# 2. Test API with access token
echo "Testing API with JWT..."
curl -X GET http://localhost:8000/api/contacts/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# 3. Test refresh token
echo "Testing refresh token..."
NEW_ACCESS=$(curl -s -X POST http://localhost:8000/api/jwt/refresh/ \
  -H "Content-Type: application/json" \
  -d "{\"refresh\": \"$REFRESH_TOKEN\"}" | jq -r .access)

echo "New Access Token: $NEW_ACCESS"

# 4. Test API with new access token
echo "Testing API with refreshed token..."
curl -X GET http://localhost:8000/api/contacts/ \
  -H "Authorization: Bearer $NEW_ACCESS"
```

## JWT vs Token Authentication Comparison

### Performance Comparison

#### Token Authentication
```python
# Every API request requires database lookup
def authenticate_token(request):
    token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    try:
        token_obj = Token.objects.get(key=token)
        return token_obj.user
    except Token.DoesNotExist:
        return None
```

#### JWT Authentication
```python
# No database lookup needed (cryptographic validation only)
def authenticate_jwt(request):
    token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    try:
        payload = jwt_decode_handler(token)
        return User.objects.get(id=payload['user_id'])
    except jwt.ExpiredSignature:
        return None
    except jwt.InvalidTokenError:
        return None
```

### When to Use Which

#### Use Token Authentication When:
- **Simple applications**: Basic CRUD APIs
- **Small user base**: Database lookup performance not critical
- **Immediate revocation needed**: Need to revoke tokens instantly
- **Development**: Easier debugging and testing

#### Use JWT Authentication When:
- **Microservices**: Multiple services need to validate tokens
- **High traffic**: Database lookups become bottleneck
- **Mobile apps**: Stateless authentication preferred
- **Scalability**: Need to handle millions of requests
- **Single Sign-On**: Share authentication across systems

### Migration Strategy

#### Support Both During Transition
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # Priority order matters
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}
```

#### Gradual Migration
1. **Phase 1**: Add JWT support alongside token auth
2. **Phase 2**: New clients use JWT, existing clients use tokens
3. **Phase 3**: Migrate existing clients to JWT
4. **Phase 4**: Remove token authentication

## JWT Security Best Practices

### 1. Token Lifetime Management
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),    # Short-lived access tokens
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),      # Longer-lived refresh tokens
    'ROTATE_REFRESH_TOKENS': True,                    # Issue new refresh tokens
    'BLACKLIST_AFTER_ROTATION': True,                 # Blacklist old refresh tokens
}
```

### 2. Secure Transmission
- **HTTPS only**: Never transmit JWT over HTTP
- **Authorization header**: Use `Authorization: Bearer <token>` format
- **Don't store in localStorage**: Use secure HTTP-only cookies for web apps
- **Short access tokens**: 5-15 minutes for access tokens

### 3. Token Storage

#### Backend (Recommended)
- **HTTP-only cookies**: Secure, not accessible via JavaScript
- **Secure flag**: Only sent over HTTPS
- **SameSite flag**: Prevent CSRF attacks

#### Frontend (Use with caution)
- **Memory**: Store in JavaScript variable (lost on refresh)
- **localStorage**: Persistent but vulnerable to XSS
- **sessionStorage**: Cleared when tab closes

### 4. Revocation Strategy
```python
# Custom JWT blacklist model
from django.db import models

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

# Custom authentication to check blacklist
class BlacklistJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        token = super().get_validated_token(raw_token)

        # Check if token is blacklisted
        jti = token.payload.get('jti')
        if BlacklistedToken.objects.filter(token=jti).exists():
            raise InvalidToken('Token is blacklisted')

        return token
```

## Advanced JWT Features

### 1. Token Blacklisting
```python
# Logout/Blacklist endpoint
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
```

### 2. Role-Based Access Control
```python
# Custom JWT with roles
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add user roles/permissions
        token['roles'] = list(user.groups.values_list('name', flat=True))
        token['permissions'] = list(user.user_permissions.values_list('codename', flat=True))

        return token

# Permission checking in views
from rest_framework.permissions import BasePermission

class HasRole(BasePermission):
    def has_permission(self, request, view):
        required_role = getattr(view, 'required_role', None)
        if not required_role:
            return True

        user_roles = request.auth.get('roles', [])
        return required_role in user_roles

# Usage in views
class AdminContactViewSet(ContactViewSet):
    required_role = 'admin'
    permission_classes = [IsAuthenticated, HasRole]
```

### 3. Multi-Device Support
```python
# Device-specific tokens
class DeviceTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add device information
        data['device_id'] = self.context.get('device_id', 'unknown')
        data['device_type'] = self.context.get('device_type', 'web')

        return data

# Store device information
class UserDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=255)
    device_type = models.CharField(max_length=50)
    last_used = models.DateTimeField(auto_now=True)
```

## Troubleshooting JWT Issues

### Common JWT Problems

#### 1. Token Not Valid
```bash
# Debug token contents
import jwt
from django.conf import settings

token = "your.jwt.token"
try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    print("Token payload:", payload)
except jwt.ExpiredSignatureError:
    print("Token has expired")
except jwt.InvalidTokenError:
    print("Token is invalid")
```

#### 2. Clock Skew Issues
```python
SIMPLE_JWT = {
    'LEEWAY': timedelta(seconds=10),  # Allow clock skew
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
}
```

#### 3. CORS Issues with JWT
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://your-frontend-domain.com",
]

CORS_ALLOW_CREDENTIALS = True  # Important for cookies
```

## Integration Examples

### Frontend (JavaScript) Integration
```javascript
// JWT Token Management
class JWTManager {
    constructor() {
        this.accessToken = localStorage.getItem('access_token');
        this.refreshToken = localStorage.getItem('refresh_token');
    }

    async login(username, password) {
        const response = await fetch('/api/jwt/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        this.setTokens(data.access, data.refresh);
        return data;
    }

    async refreshAccessToken() {
        const response = await fetch('/api/jwt/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: this.refreshToken }),
        });

        if (response.ok) {
            const data = await response.json();
            this.accessToken = data.access;
            localStorage.setItem('access_token', this.accessToken);
            return data.access;
        } else {
            this.logout();
            throw new Error('Failed to refresh token');
        }
    }

    async authenticatedFetch(url, options = {}) {
        let headers = {
            ...options.headers,
            'Authorization': `Bearer ${this.accessToken}`,
        };

        let response = await fetch(url, { ...options, headers });

        // If access token expired, try to refresh
        if (response.status === 401) {
            try {
                await this.refreshAccessToken();
                headers['Authorization'] = `Bearer ${this.accessToken}`;
                response = await fetch(url, { ...options, headers });
            } catch (error) {
                this.logout();
                throw error;
            }
        }

        return response;
    }

    setTokens(access, refresh) {
        this.accessToken = access;
        this.refreshToken = refresh;
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
    }

    logout() {
        this.accessToken = null;
        this.refreshToken = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }
}

// Usage
const jwtManager = new JWTManager();

// Login
await jwtManager.login('username', 'password');

// API call with automatic token refresh
const response = await jwtManager.authenticatedFetch('/api/contacts/');
```

## Key Concepts Covered

### JWT vs Token Authentication
- **Stateless vs Stateful**: JWT doesn't require database lookups
- **Scalability**: JWT better for distributed systems
- **Revocation**: Token auth easier to revoke instantly
- **Size**: JWT tokens are larger than database tokens

### JWT Structure
- **Header**: Algorithm and token type
- **Payload**: Claims (user data, expiration)
- **Signature**: Cryptographic verification

### JWT Security
- **Short access tokens**: 5-15 minutes
- **Refresh tokens**: Longer duration
- **Token rotation**: Issue new refresh tokens
- **HTTPS required**: Never transmit over HTTP

### JWT Configuration
- **Lifetime settings**: Configure token expiration
- **Authentication classes**: Multiple auth methods
- **Custom claims**: Add user data to tokens
- **Token verification**: Validate token integrity

## Success Criteria
- [ ] JWT authentication configured successfully
- [ ] Can obtain JWT token pairs
- [ ] Access tokens work for API requests
- [ ] Refresh tokens work correctly
- [ ] Token expiration handled properly
- [ ] Both JWT and token authentication work together

## Common Issues and Solutions

### Token Validation Failures
- **Expired tokens**: Implement refresh token logic
- **Invalid signature**: Check secret key configuration
- **Clock skew**: Add leeway to JWT settings

### CORS Problems
- **Pre-flight requests**: Handle OPTIONS requests
- **Credentials**: Set CORS_ALLOW_CREDENTIALS=True
- **Origins**: Configure allowed origins properly

### Performance Issues
- **Token validation**: Implement JWT validation caching
- **Database queries**: Optimize user lookup
- **Token size**: Minimize payload data

## Conclusion

JWT authentication provides a scalable, stateless authentication solution that's ideal for modern web applications, mobile apps, and microservices architectures. While it introduces more complexity than traditional token authentication, the benefits in scalability and performance make it an excellent choice for production applications.

The key to successful JWT implementation is understanding the security implications and implementing proper token lifecycle management, including refresh tokens, blacklisting, and secure storage practices.

## Additional Resources

- [JWT Specification (RFC 7519)](https://tools.ietf.org/html/rfc7519)
- [JWT.io](https://jwt.io/) - JWT debugger and documentation
- [Simple JWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)