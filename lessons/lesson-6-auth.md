# Lesson 6: Authentication Setup

## Learning Goals
- Understand token-based authentication workflow
- Learn the difference between session and token authentication
- Set up user accounts and authentication tokens
- Test authenticated and unauthenticated API access
- Configure DRF browsable API login

## What is Authentication in Web APIs?

**Authentication** is the process of verifying who a user is. In APIs, this ensures that:
- Only authorized users can access the API
- Users can only access their own data
- API requests are properly tracked and secured

## Authentication Methods Available

### Token Authentication (Primary Method)
- **How it works**: Client sends token in HTTP header
- **Best for**: Mobile apps, single-page applications, external services
- **Stateless**: No server-side session storage
- **Simple**: Easy to implement and use

### Session Authentication (Secondary Method)
- **How it works**: Uses Django's session framework
- **Best for**: Traditional web applications, browsable API
- **Stateful**: Requires server-side session storage
- **Browser-friendly**: Works automatically with browser cookies

## Token Authentication Workflow

### Step 1: User Registration/Login
```bash
POST /api-token/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "secure_password"
}
```

### Step 2: Receive Token
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Step 3: Use Token in Requests
```bash
GET /api/contacts/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## Setting Up Authentication

### Create Superuser
```bash
python manage.py createsuperuser
```

Follow the prompts:
- **Username**: Choose a memorable username
- **Email**: Your email address
- **Password**: Choose a strong password
- **Password confirmation**: Re-enter the password

### Create Regular Users (Optional)
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# Create a regular user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)
print(f"Created user: {user.username}")
```

## Our Authentication Configuration

### settings.py Configuration
```python
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### What This Configuration Does

#### TokenAuthentication
- **Primary method**: Token-based authentication
- **HTTP Header**: `Authorization: Token <token>`
- **Best for**: API clients, mobile apps, SPAs

#### SessionAuthentication
- **Secondary method**: Django sessions
- **Browser cookies**: Automatic in browsers
- **Best for**: DRF browsable API, web applications

#### IsAuthenticated Permission
- **Required**: User must be authenticated
- **Applies to**: All endpoints by default
- **Override**: Can be overridden per ViewSet

## Testing Authentication

### Testing with curl

#### 1. Test Unauthenticated Access (Should Fail)
```bash
curl -i http://localhost:8000/api/contacts/
```

**Expected Response:**
```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{"detail":"Authentication credentials were not provided."}
```

#### 2. Get Authentication Token
```bash
curl -X POST http://localhost:8000/api-token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**Expected Response:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

#### 3. Use Token for Authenticated Request
```bash
curl -X GET http://localhost:8000/api/contacts/ \
  -H "Authorization: Token your_token_here"
```

**Expected Response:**
```json
{
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
}
```

#### 4. Create Contact with Authentication
```bash
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890"
  }'
```

**Expected Response:**
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "owner": "your_username"
}
```

### Testing with Django Shell

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from contacts.models import Contact

# Create user and token
user = User.objects.create_user('testuser', 'test@example.com', 'password123')
token, created = Token.objects.get_or_create(user=user)

print(f"User: {user.username}")
print(f"Token: {token.key}")

# Create contact for user
contact = Contact.objects.create(
    owner=user,
    name='Test Contact',
    email='test@example.com',
    phone='555-1234'
)

print(f"Created contact: {contact}")
print(f"Owner: {contact.owner.username}")
```

## DRF Browsable API Authentication

### Accessing the Browsable API
1. Start development server: `python manage.py runserver`
2. Visit: `http://localhost:8000/api/contacts/`
3. You should see "Authentication credentials were not provided"

### Logging into Browsable API

#### Method 1: Using api-auth Login
1. Visit: `http://localhost:8000/api-auth/login/`
2. Enter your username and password
3. Redirected back to API with authentication

#### Method 2: Using Token
1. Visit: `http://localhost:8000/api/contacts/`
2. Click the "Authenticate" button (top right)
3. Enter your token in the format: `Token your_token_here`

### Benefits of Browsable API
- **Interactive testing**: Try API endpoints in browser
- **API documentation**: See available endpoints and methods
- **Form validation**: Test data validation with forms
- **Error handling**: See error messages clearly

## Understanding Token Authentication

### How Tokens Are Created

#### Automatic Creation
```python
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Token is created automatically when user is created
user = User.objects.create_user('username', 'email', 'password')
token = Token.objects.get(user=user)
print(f"Token: {token.key}")
```

#### Manual Token Creation
```python
# Create token manually if needed
token = Token.objects.create(user=user)
print(f"Created token: {token.key}")
```

### Token Storage and Security
- **Server storage**: Tokens stored in database
- **Client storage**: Client stores token (localStorage, secure storage)
- **Security**: Tokens should be transmitted over HTTPS
- **Expiration**: Tokens don't expire by default (but can be configured)

### Token vs Session Authentication

#### Token Authentication
✅ **Pros:**
- Stateless (no server-side session)
- Good for mobile apps and SPAs
- Scalable across multiple servers
- Simple HTTP header authentication

❌ **Cons:**
- Manual token management required
- Tokens don't expire by default
- Revocation requires database access

#### Session Authentication
✅ **Pros:**
- Automatic browser cookie handling
- Built-in Django session management
- Easy logout and invalidation
- CSRF protection built-in

❌ **Cons:**
- Stateful (requires server-side storage)
- Not ideal for mobile apps/SPAs
- Session scalability issues
- Requires CSRF tokens for POST/PUT/DELETE

## Managing Authentication Tokens

### View All Tokens
```bash
python manage.py shell
```

```python
from rest_framework.authtoken.models import Token

# Show all tokens
for token in Token.objects.all():
    print(f"User: {token.user.username}, Token: {token.key[:8]}...")
```

### Regenerate Token
```python
# Delete existing token
Token.objects.filter(user=user).delete()

# Create new token
token = Token.objects.create(user=user)
print(f"New token: {token.key}")
```

### Delete Token (Logout)
```python
# Delete user's token
Token.objects.filter(user=user).delete()
print("Token deleted - user logged out")
```

## Common Authentication Issues

### 401 Unauthorized
**Problem:** "Authentication credentials were not provided"

**Solutions:**
1. Check that token is being sent correctly
2. Verify token format: `Authorization: Token <token>`
3. Ensure token exists in database
4. Check user account is active

### 403 Forbidden
**Problem:** "You do not have permission to perform this action"

**Solutions:**
1. Check permission classes in ViewSet
2. Verify object ownership (IsOwnerOrReadOnly)
3. Ensure user is authenticated
4. Check user account permissions

### Invalid Token
**Problem:** Token is not accepted

**Solutions:**
1. Verify token exists in database
2. Check token format (no extra spaces)
3. Ensure token belongs to active user
4. Regenerate token if necessary

### CORS Issues (Frontend Testing)
**Problem:** Browser blocks API requests from different origins

**Solutions:**
1. Install django-cors-headers
2. Configure CORS settings
3. Test with curl instead of browser
4. Use same-origin testing

## Security Best Practices

### Token Security
- **HTTPS**: Always transmit tokens over HTTPS
- **Storage**: Store tokens securely on client side
- **Expiration**: Consider implementing token expiration
- **Revocation**: Provide method to revoke tokens

### User Security
- **Strong passwords**: Enforce password requirements
- **Account protection**: Rate limiting, account lockout
- **Permission principles**: Least privilege principle
- **Audit logging**: Log authentication attempts

### API Security
- **HTTPS only**: Disable HTTP in production
- **CORS**: Configure properly for your domain
- **Rate limiting**: Prevent abuse
- **Input validation**: Validate all input data

## Testing Authentication Flow End-to-End

### Complete Workflow Test
```bash
# 1. Start the server
python manage.py runserver

# 2. Create a superuser if not exists
python manage.py createsuperuser

# 3. Test unauthenticated access (should fail)
curl -i http://localhost:8000/api/contacts/

# 4. Get auth token
TOKEN=$(curl -s -X POST http://localhost:8000/api-token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}' \
  | jq -r .token)

# 5. Test authenticated access
curl -X GET http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN"

# 6. Create a contact
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Contact", "email": "test@example.com"}'

# 7. List contacts (should show the new contact)
curl -X GET http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN"
```

## Key Concepts Covered

### Authentication Methods
- **Token authentication**: Stateless, good for APIs
- **Session authentication**: Stateful, good for browsers
- **Multiple methods**: Can use both simultaneously

### Token Management
- **Creation**: Automatic with user creation
- **Storage**: Database storage with user relation
- **Usage**: HTTP Authorization header
- **Security**: HTTPS transmission required

### Permission System
- **IsAuthenticated**: Default permission class
- **Custom permissions**: Object-level access control
- **Multiple permissions**: Applied in sequence

### Testing Authentication
- **Unauthenticated tests**: Verify API is protected
- **Authenticated tests**: Verify API works with valid auth
- **Error handling**: Understand 401 vs 403 errors

## Success Criteria
- [ ] Superuser account created successfully
- [ ] Can obtain authentication token
- [ ] Unauthenticated requests are blocked (401)
- [ ] Authenticated requests work correctly
- [ ] DRF browsable API login works
- [ ] Contact CRUD operations work with authentication

## Common Issues and Solutions

### Token Problems
- **Invalid token**: Check token format and database existence
- **Missing token**: Ensure token is sent in Authorization header
- **Expired token**: Regenerate token if needed

### Permission Problems
- **403 Forbidden**: Check user permissions and object ownership
- **401 Unauthorized**: Check authentication method and token validity

### Configuration Problems
- **Settings errors**: Verify REST_FRAMEWORK configuration
- **App registration**: Ensure authtoken app is installed

## Next Steps
In the next lesson, we'll perform comprehensive API testing with various tools and scenarios.

## Additional Resources
- [DRF Authentication Documentation](https://www.django-rest-framework.org/api-guide/authentication/)
- [DRF Permissions Documentation](https://www.django-rest-framework.org/api-guide/permissions/)
- [Token Authentication Best Practices](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)