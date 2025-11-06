# Lesson 3: DRF Serializers

## Learning Goals
- Understand what serialization is and why it's needed
- Learn the difference between Serializer and ModelSerializer
- Create custom validation for serializer fields
- Test serializers in Django shell
- Understand data conversion between Python objects and JSON

## What is Serialization?

**Serialization** is the process of converting data structures or object state into a format that can be stored or transmitted and reconstructed later.

**In Web APIs:**
- Convert Python objects (Django models) to JSON (for API responses)
- Convert JSON data to Python objects (for API requests)
- Validate incoming data before converting to objects

## Why Do We Need Serializers?

### API Response Serialization
```python
# Django Model instance
contact = Contact.objects.get(id=1)
# contact.name = "John Doe", contact.email = "john@example.com"

# API Response (JSON)
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "owner": "testuser"
}
```

### API Request Validation
```python
# Incoming JSON
{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "555-1234"
}

# Validated and converted to Contact object
contact = Contact(name="Jane Smith", email="jane@example.com", phone="555-1234")
```

## Our ContactSerializer

Let's examine our serializer in `contacts/serializers.py`:

```python
from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'created_at', 'updated_at', 'owner']
        extra_kwargs = {
            'email': {'validators': []},
        }
```

## ModelSerializer vs Serializer

### ModelSerializer (Recommended for Beginners)
```python
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone']
```

**Advantages:**
- Automatically generates fields from model
- Includes default validators based on model fields
- Less code to write and maintain
- Built-in create() and update() methods

### Serializer (More Control)
```python
class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False)

    def create(self, validated_data):
        return Contact.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        # ... update other fields
        instance.save()
        return instance
```

**Advantages:**
- Complete control over field definitions
- Can serialize data not tied to Django models
- More flexible for complex custom logic

## Serializer Fields and Options

### Field Types
- **CharField**: Text data with length limits
- **EmailField**: CharField with email validation
- **IntegerField**: Whole numbers
- **DecimalField**: Decimal numbers with precision
- **DateTimeField**: Date and time
- **BooleanField**: True/False values
- **ListField**: Arrays of data

### Common Field Options
- **required**: Whether field is required (default: True)
- **allow_null**: Whether None is allowed
- **default**: Default value if not provided
- **read_only**: Field is included in output but not in input
- **write_only**: Field is used for input but not in output
- **validators**: List of validation functions

## Custom Fields and Read-Only Fields

### Our owner Field
```python
owner = serializers.ReadOnlyField(source='owner.username')
```
- **ReadOnlyField**: Cannot be set by the user
- **source='owner.username'**: Gets the username from the owner object
- **Purpose**: Shows who owns the contact without allowing changes

### Field Selection
```python
fields = ['id', 'name', 'email', 'phone', 'created_at', 'updated_at', 'owner']
```
- **Explicit field list**: Controls exactly what's in API responses
- **Security**: Don't expose sensitive fields
- **Performance**: Only include needed data

## Custom Validation

### Field-Level Validation
```python
def validate_email(self, value):
    """Custom email validation logic"""
    if '@example.com' in value.lower():
        raise serializers.ValidationError("Example.com emails are not allowed")
    return value
```

### How Field Validation Works
1. Django runs built-in field validation
2. Field-specific validation methods are called
3. Returns cleaned value or raises ValidationError

### More Validation Examples
```python
def validate_phone(self, value):
    """Phone number validation"""
    if value and not value.replace('-', '').replace(' ', '').isdigit():
        raise serializers.ValidationError("Phone should contain only digits")
    return value

def validate_name(self, value):
    """Name validation"""
    if not value or len(value.strip()) < 2:
        raise serializers.ValidationError("Name must be at least 2 characters")
    return value.strip()
```

### Object-Level Validation
```python
def validate(self, data):
    """Validate multiple fields together"""
    name = data.get('name', '')
    email = data.get('email', '')

    if name.lower() == email.split('@')[0].lower():
        raise serializers.ValidationError(
            "Name cannot be the same as email username"
        )
    return data
```

## Extra Kwargs and Validators

### Removing Default Validators
```python
extra_kwargs = {
    'email': {'validators': []},
}
```
**Why?**
- Django EmailField has built-in validators
- We want to provide custom error messages
- More control over validation logic

### Adding Custom Validators
```python
from rest_framework.validators import UniqueValidator

email = serializers.EmailField(
    validators=[
        UniqueValidator(
            queryset=Contact.objects.all(),
            message="This email already exists"
        )
    ]
)
```

## Testing Serializers in Django Shell

```bash
python manage.py shell
```

### Serialization (Model to JSON)
```python
from contacts.models import Contact
from contacts.serializers import ContactSerializer
from django.contrib.auth.models import User

# Get a user and contact
user = User.objects.first()
contact = Contact.objects.filter(owner=user).first()

# Serialize the contact
serializer = ContactSerializer(contact)
print(serializer.data)
# Output: {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', ...}
```

### Deserialization (JSON to Model)
```python
# Data to create a new contact
data = {
    'name': 'Jane Smith',
    'email': 'jane@example.com',
    'phone': '555-1234'
}

serializer = ContactSerializer(data=data)
print(serializer.is_valid())  # True if data is valid
print(serializer.validated_data)  # Cleaned data
print(serializer.errors)  # Validation errors

# Save to database
if serializer.is_valid():
    contact = serializer.save()
    print(f"Created: {contact}")
```

### Testing Validation
```python
# Test invalid email
invalid_data = {
    'name': 'Test User',
    'email': 'test@example.com',  # Will be blocked by our validation
    'phone': '123'
}

serializer = ContactSerializer(data=invalid_data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'email': ['Example.com emails are not allowed']}
```

## Serializer Context

### Passing Context
```python
# In views.py
serializer = ContactSerializer(contact, context={'request': request})
```

### Using Context in Validation
```python
def validate_email(self, value):
    request = self.context.get('request')
    if request and request.user:
        # Check if email already exists for this user
        if Contact.objects.filter(owner=request.user, email=value).exists():
            raise serializers.ValidationError("Email already exists for your account")
    return value
```

## Common Serialization Patterns

### Nested Serialization
```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ContactSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'owner']
```

### Method Fields
```python
class ContactSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.name} ({obj.email})"
```

## Key Concepts Covered

### Serialization Process
- **Model → JSON**: Convert Django objects to API responses
- **JSON → Model**: Convert API requests to Django objects
- **Validation**: Ensure data integrity before conversion

### ModelSerializer Benefits
- **Automatic field generation**: Less code to write
- **Built-in validation**: Based on model field definitions
- **CRUD operations**: Automatic create/update methods

### Custom Validation
- **Field-level**: Validate individual fields
- **Object-level**: Validate multiple fields together
- **Custom error messages**: User-friendly validation feedback

## Success Criteria
- [ ] ContactSerializer created successfully
- [ ] Can serialize Contact objects to JSON
- [ ] Can deserialize JSON to Contact objects
- [ ] Custom validation works correctly
- [ ] Error messages are clear and helpful
- [ ] All fields properly configured

## Common Issues

### Validation Errors
1. **Silent failures**: Always check `serializer.is_valid()`
2. **Missing required fields**: Include all required fields in data
3. **Type mismatches**: Ensure data types match field expectations

### Field Configuration
1. **Wrong field types**: Use appropriate field types
2. **Missing source parameter**: For related fields
3. **Extra fields not in Meta.fields**: Include all fields in fields list

## Next Steps
In the next lesson, we'll create DRF ViewSets to handle HTTP requests and provide CRUD operations.

## Additional Resources
- [DRF Serializer Documentation](https://www.django-rest-framework.org/api-guide/serializers/)
- [DRF Field Documentation](https://www.django-rest-framework.org/api-guide/fields/)
- [DRF Validation Documentation](https://www.django-rest-framework.org/api-guide/validators/)