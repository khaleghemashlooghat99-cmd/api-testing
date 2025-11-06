from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for Contact model with custom validation.
    Handles conversion between Contact instances and JSON data.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'created_at', 'updated_at', 'owner']
        extra_kwargs = {
            'email': {'validators': []},  # Remove default validators for custom error messages
        }

    def validate_email(self, value):
        """
        Custom email validation logic.
        Prevents certain domains and validates email format.
        """
        # Example validation: block example.com emails
        if '@example.com' in value.lower():
            raise serializers.ValidationError("Example.com emails are not allowed")

        # Basic email format validation (additional to built-in)
        if not value or '@' not in value:
            raise serializers.ValidationError("Please enter a valid email address")

        return value

    def validate_phone(self, value):
        """
        Custom phone number validation.
        Ensures phone number contains only digits and basic formatting.
        """
        # Allow empty phone numbers (field is optional)
        if not value:
            return value

        # Remove common formatting characters for validation
        clean_phone = value.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')

        # Check if remaining characters are digits
        if not clean_phone.isdigit():
            raise serializers.ValidationError("Phone number should contain only digits")

        # Check minimum length (after cleaning)
        if len(clean_phone) < 10:
            raise serializers.ValidationError("Phone number should have at least 10 digits")

        return value

    def validate_name(self, value):
        """
        Custom name validation.
        Ensures name is not empty and has reasonable length.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Name cannot be empty")

        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name should have at least 2 characters")

        return value.strip()

    def validate(self, data):
        """
        Object-level validation.
        Can validate multiple fields together.
        """
        # Example: Check if email and name combination makes sense
        name = data.get('name', '')
        email = data.get('email', '')

        # Basic validation to prevent obviously fake data
        if name.lower() == email.split('@')[0].lower():
            raise serializers.ValidationError(
                "Name cannot be the same as email username. Please provide a real name."
            )

        return data