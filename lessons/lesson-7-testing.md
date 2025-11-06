# Lesson 7: API Testing

## Learning Goals
- Learn comprehensive API testing with curl and Postman
- Test all CRUD operations thoroughly
- Understand HTTP methods and status codes
- Test authentication and authorization
- Validate error handling and data validation
- Test cross-user data isolation

## Why API Testing is Important

API testing ensures that:
- **Functionality works correctly**: All endpoints behave as expected
- **Security is enforced**: Authentication and authorization work
- **Data integrity is maintained**: Validation prevents bad data
- **Error handling is proper**: Appropriate status codes and messages
- **Performance is acceptable**: Response times and load handling

## Testing Tools Overview

### curl (Command Line)
- **Built into most systems**: No installation needed
- **Scriptable**: Easy to automate
- **Low-level**: Complete control over HTTP requests
- **Universal**: Works on all platforms

### Postman (GUI Tool)
- **User-friendly**: Visual interface
- **Request saving**: Organize and save requests
- **Environments**: Manage different configurations
- **Testing features**: Built-in test scripting

### DRF Browsable API
- **Interactive**: Test directly in browser
- **Documentation**: Auto-generated API docs
- **Forms**: Easy data entry and validation testing
- **Convenient**: Quick testing during development

## Preparing for Testing

### Start Development Server
```bash
python manage.py runserver
```

### Get Authentication Token
```bash
# Get your token once and save it
export TOKEN=$(curl -s -X POST http://localhost:8000/api-token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}' \
  | jq -r .token)

echo "Token: $TOKEN"
```

### Alternative: Manual Token Management
```bash
# Save token to a file
echo "your_token_here" > token.txt

# Use token in commands
TOKEN=$(cat token.txt)
```

## Testing Scenarios

### 1. Unauthenticated Access Tests (Should Fail)

#### Test 1: List Contacts Without Authentication
```bash
curl -i -X GET http://localhost:8000/api/contacts/
```

**Expected Response:**
```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json
Allow: GET, POST, HEAD, OPTIONS

{"detail":"Authentication credentials were not provided."}
```

#### Test 2: Create Contact Without Authentication
```bash
curl -i -X POST http://localhost:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "email": "test@example.com"}'
```

**Expected Response:**
```http
HTTP/1.1 401 Unauthorized
{"detail":"Authentication credentials were not provided."}
```

### 2. Authentication Flow Tests

#### Test 3: Get Authentication Token
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

#### Test 4: Invalid Credentials
```bash
curl -X POST http://localhost:8000/api-token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "wrong_user", "password": "wrong_password"}'
```

**Expected Response:**
```http
HTTP/1.1 400 Bad Request
{"non_field_errors":["Unable to log in with provided credentials."]}
```

### 3. CRUD Operation Tests

#### Test 5: List Empty Contacts
```bash
curl -X GET http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN"
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

#### Test 6: Create Contact (POST)
```bash
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN" \
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

#### Test 7: Create Multiple Contacts
```bash
# Create second contact
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "555-1234"
  }'

# Create third contact (without phone)
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bob Johnson",
    "email": "bob@example.com"
  }'
```

#### Test 8: List All Contacts
```bash
curl -X GET http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN"
```

**Expected Response:**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "phone": "",
            "created_at": "2024-01-15T10:32:00Z",
            "updated_at": "2024-01-15T10:32:00Z",
            "owner": "your_username"
        },
        {
            "id": 2,
            "name": "Jane Smith",
            "email": "jane@example.com",
            "phone": "555-1234",
            "created_at": "2024-01-15T10:31:00Z",
            "updated_at": "2024-01-15T10:31:00Z",
            "owner": "your_username"
        },
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "123-456-7890",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "owner": "your_username"
        }
    ]
}
```

#### Test 9: Retrieve Specific Contact (GET)
```bash
curl -X GET http://localhost:8000/api/contacts/1/ \
  -H "Authorization: Token $TOKEN"
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

#### Test 10: Update Contact (PUT)
```bash
curl -X PUT http://localhost:8000/api/contacts/1/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Johnathan Doe",
    "email": "john.doe@example.com",
    "phone": "098-765-4321"
  }'
```

**Expected Response:**
```json
{
    "id": 1,
    "name": "Johnathan Doe",
    "email": "john.doe@example.com",
    "phone": "098-765-4321",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:33:00Z",
    "owner": "your_username"
}
```

#### Test 11: Partial Update Contact (PATCH)
```bash
curl -X PATCH http://localhost:8000/api/contacts/2/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"phone": "555-9876"}'
```

**Expected Response:**
```json
{
    "id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "555-9876",
    "created_at": "2024-01-15T10:31:00Z",
    "updated_at": "2024-01-15T10:34:00Z",
    "owner": "your_username"
}
```

#### Test 12: Delete Contact (DELETE)
```bash
curl -X DELETE http://localhost:8000/api/contacts/3/ \
  -H "Authorization: Token $TOKEN"
```

**Expected Response:**
```http
HTTP/1.1 204 No Content
```

Verify deletion:
```bash
curl -X GET http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN"
```

### 4. Data Validation Tests

#### Test 13: Invalid Email Format
```bash
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "invalid-email",
    "phone": "123-456"
  }'
```

**Expected Response:**
```http
HTTP/1.1 400 Bad Request
{"email":["Enter a valid email address."]}
```

#### Test 14: Missing Required Fields
```bash
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "123-456"
  }'
```

**Expected Response:**
```http
HTTP/1.1 400 Bad Request
{"name":["This field is required."],"email":["This field is required."]}
```

#### Test 15: Custom Validation (Blocked Domain)
```bash
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com"
  }'
```

**Expected Response:**
```http
HTTP/1.1 400 Bad Request
{"email":["Example.com emails are not allowed"]}
```

#### Test 16: Invalid Phone Number
```bash
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@valid.com",
    "phone": "abc-def"
  }'
```

**Expected Response:**
```http
HTTP/1.1 400 Bad Request
{"phone":["Phone number should contain only digits"]}
```

### 5. User Isolation Tests

#### Test 17: Create Two Users and Test Data Isolation
```bash
# Create second user and get token
USER2_TOKEN=$(curl -s -X POST http://localhost:8000/api-token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user2", "password": "password123"}' \
  | jq -r .token)

# Create contact with user2
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $USER2_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "User Two Contact",
    "email": "user2@example.com"
  }'

# List contacts with user1 token (should only see user1 contacts)
curl -X GET http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN"

# Try to access user2's contact with user1 token (should fail)
curl -i -X GET http://localhost:8000/api/contacts/4/ \
  -H "Authorization: Token $TOKEN"
```

**Expected Response for unauthorized access:**
```http
HTTP/1.1 404 Not Found
```

### 6. Error Handling Tests

#### Test 18: Access Non-Existent Contact
```bash
curl -i -X GET http://localhost:8000/api/contacts/999/ \
  -H "Authorization: Token $TOKEN"
```

**Expected Response:**
```http
HTTP/1.1 404 Not Found
{"detail":"Not found."}
```

#### Test 19: Invalid HTTP Method
```bash
curl -i -X TRACE http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN"
```

**Expected Response:**
```http
HTTP/1.1 405 Method Not Allowed
Allow: GET, POST, HEAD, OPTIONS
{"detail":"Method \"TRACE\" not allowed."}
```

## HTTP Status Codes Reference

### Success Codes
- **200 OK**: Request successful (GET, PUT, PATCH)
- **201 Created**: Resource created successfully (POST)
- **204 No Content**: Request successful, no content returned (DELETE)

### Client Error Codes
- **400 Bad Request**: Invalid request data or validation errors
- **401 Unauthorized**: Authentication required but not provided
- **403 Forbidden**: Authenticated but no permission
- **404 Not Found**: Resource not found
- **405 Method Not Allowed**: HTTP method not supported

### Server Error Codes
- **500 Internal Server Error**: Server-side error (should be rare)

## Testing with Postman

### Setting up Postman

#### 1. Environment Variables
Create an environment with these variables:
- `base_url`: `http://localhost:8000`
- `token`: Your authentication token

#### 2. Authorization Setup
In Authorization tab:
- Type: `Bearer Token`
- Token: `{{token}}`

#### 3. Creating Collections
Organize requests by functionality:
- Authentication
- Contact CRUD
- Error Testing
- Validation Testing

### Sample Postman Requests

#### Get Token Request
```
POST {{base_url}}/api-token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

#### List Contacts Request
```
GET {{base_url}}/api/contacts/
Authorization: Token {{token}}
```

#### Create Contact Request
```
POST {{base_url}}/api/contacts/
Authorization: Token {{token}}
Content-Type: application/json

{
  "name": "New Contact",
  "email": "contact@example.com",
  "phone": "123-456"
}
```

## Automated Testing Scripts

### Bash Script for Basic Testing
```bash
#!/bin/bash

# API Testing Script
BASE_URL="http://localhost:8000"
USERNAME="your_username"
PASSWORD="your_password"

echo "🚀 Starting API Tests..."

# Get authentication token
echo "📝 Getting authentication token..."
TOKEN=$(curl -s -X POST "$BASE_URL/api-token/" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}" \
  | jq -r .token)

if [ "$TOKEN" == "null" ]; then
  echo "❌ Failed to get authentication token"
  exit 1
fi

echo "✅ Authentication successful"

# Test unauthenticated access
echo "🔒 Testing unauthenticated access..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/contacts/")
if [ "$RESPONSE" == "401" ]; then
  echo "✅ Unauthenticated access properly blocked"
else
  echo "❌ Unauthenticated access not blocked (HTTP $RESPONSE)"
fi

# Test creating contact
echo "👤 Creating test contact..."
CONTACT_ID=$(curl -s -X POST "$BASE_URL/api/contacts/" \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Contact", "email": "test@example.com"}' \
  | jq -r .id)

if [ "$CONTACT_ID" != "null" ]; then
  echo "✅ Contact created successfully (ID: $CONTACT_ID)"
else
  echo "❌ Failed to create contact"
fi

# Test listing contacts
echo "📋 Testing contact listing..."
COUNT=$(curl -s -X GET "$BASE_URL/api/contacts/" \
  -H "Authorization: Token $TOKEN" \
  | jq -r .count)

echo "✅ Found $COUNT contacts"

echo "🎉 API testing completed!"
```

## Testing Checklist

### Functionality Tests
- [ ] Unauthenticated access is blocked
- [ ] Authentication with correct credentials works
- [ ] Authentication with wrong credentials fails
- [ ] Can create contacts (POST)
- [ ] Can list contacts (GET)
- [ ] Can retrieve specific contact (GET)
- [ ] Can update contact (PUT/PATCH)
- [ ] Can delete contact (DELETE)

### Data Validation Tests
- [ ] Required field validation works
- [ ] Email format validation works
- [ ] Custom validation rules work
- [ ] Phone number validation works
- [ ] Length validation works

### Security Tests
- [ ] Users can only see their own contacts
- [ ] Users cannot modify others' contacts
- [ ] Token authentication works
- [ ] Invalid tokens are rejected

### Error Handling Tests
- [ ] 404 errors for non-existent resources
- [ ] 405 errors for unsupported methods
- [ ] 400 errors for invalid data
- [ ] Clear error messages

## Performance Considerations

### Response Time Testing
```bash
# Test response time for list endpoint
time curl -s -X GET http://localhost:8000/api/contacts/ \
  -H "Authorization: Token $TOKEN" > /dev/null
```

### Load Testing (Simple)
```bash
# Simple load test - 10 concurrent requests
for i in {1..10}; do
  curl -s -X GET http://localhost:8000/api/contacts/ \
    -H "Authorization: Token $TOKEN" > /dev/null &
done
wait
echo "10 requests completed"
```

## Key Concepts Covered

### API Testing Tools
- **curl**: Command-line HTTP testing
- **Postman**: GUI testing and organization
- **DRF Browsable API**: Interactive browser testing

### HTTP Testing
- **Methods**: GET, POST, PUT, PATCH, DELETE
- **Status codes**: Success, client errors, server errors
- **Headers**: Authentication, content type
- **Body**: Request/response data

### Validation Testing
- **Field validation**: Required fields, formats, lengths
- **Custom validation**: Business logic validation
- **Error messages**: Clear, user-friendly feedback

### Security Testing
- **Authentication**: Valid and invalid credentials
- **Authorization**: User isolation and permissions
- **Data protection**: Users can't access others' data

## Success Criteria
- [ ] All CRUD operations work correctly
- [ ] Authentication is properly enforced
- [ ] Data validation catches invalid inputs
- [ ] User isolation works correctly
- [ ] Error handling provides appropriate responses
- [ ] API responses follow REST conventions

## Common Testing Issues

### Authentication Failures
- **Token not sent**: Check Authorization header format
- **Invalid token**: Verify token is correct and not expired
- **Wrong method**: Use POST for token endpoint

### Data Validation Issues
- **Unexpected validation errors**: Check serializer rules
- **Missing fields**: Verify all required fields are included
- **Format errors**: Ensure data types are correct

### User Isolation Problems
- **Users see others' data**: Check get_queryset filtering
- **Can edit others' data**: Check object permissions
- **Cross-user access**: Test with multiple users

## Next Steps
In the next lesson, we'll create comprehensive documentation and explore next steps for extending this API.

## Additional Resources
- [RESTful API Testing Best Practices](https://restfulapi.net/api-testing-best-practices/)
- [curl Tutorial](https://curl.se/docs/manual.html)
- [Postman Learning Center](https://learning.postman.com/)