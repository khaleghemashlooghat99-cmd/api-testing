# Django REST Framework Contact API

A complete Django REST Framework API for managing contacts with full CRUD operations, token-based authentication, and comprehensive documentation. This project serves as an educational resource for learning DRF development step by step.

## 🚀 Features

- ✅ **Full CRUD Operations** - Create, Read, Update, Delete contacts
- ✅ **Token-Based Authentication** - Secure API access with authentication tokens
- ✅ **User-Specific Data** - Users can only access their own contacts
- ✅ **Data Validation** - Comprehensive input validation with custom rules
- ✅ **Error Handling** - Proper HTTP status codes and error messages
- ✅ **DRF Browsable API** - Interactive HTML interface for testing
- ✅ **Django Admin** - Built-in admin interface for data management
- ✅ **Educational Content** - 8 detailed lessons explaining every concept
- ✅ **JWT Support** - Bonus lesson on JWT authentication
- ✅ **Production Ready** - Best practices and security considerations

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Educational Content](#educational-content)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🎯 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd api-testing
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Run development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - API endpoints: http://localhost:8000/api/
   - Admin interface: http://localhost:8000/admin/
   - Browsable API: http://localhost:8000/api/contacts/

## 📁 Project Structure

```
api-testing/
├── api_project/                 # Django project configuration
│   ├── __init__.py
│   ├── settings.py              # Django settings with DRF configuration
│   ├── urls.py                  # Main URL routing
│   └── wsgi.py                  # WSGI configuration
├── contacts/                    # Contacts Django app
│   ├── __init__.py
│   ├── admin.py                 # Django admin configuration
│   ├── apps.py                  # App configuration
│   ├── migrations/              # Database migrations
│   ├── models.py                # Contact model definition
│   ├── serializers.py           # DRF serializers with validation
│   ├── tests.py                 # Test cases
│   ├── urls.py                  # App URL configuration
│   └── views.py                 # DRF ViewSets with permissions
├── lessons/                     # Educational content
│   ├── lesson-1-setup.md        # Django project setup
│   ├── lesson-2-models.md       # Models and database
│   ├── lesson-3-serializers.md  # DRF serializers
│   ├── lesson-4-views.md        # ViewSets and permissions
│   ├── lesson-5-urls.md         # URL routing and routers
│   ├── lesson-6-auth.md         # Authentication setup
│   ├── lesson-7-testing.md      # API testing
│   ├── lesson-8-documentation.md # Documentation and next steps
│   └── bonus-jwt-auth.md        # JWT authentication bonus
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 📚 API Documentation

### Authentication Endpoints

#### Obtain Authentication Token
```http
POST /api-token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Contact Endpoints

All contact endpoints require authentication via the `Authorization: Token <token>` header.

#### List Contacts
```http
GET /api/contacts/
Authorization: Token your_token_here
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "123-456-7890",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "owner": "johndoe"
    }
  ]
}
```

#### Create Contact
```http
POST /api/contacts/
Authorization: Token your_token_here
Content-Type: application/json

{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "555-1234"
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "555-1234",
  "created_at": "2024-01-15T10:35:00Z",
  "updated_at": "2024-01-15T10:35:00Z",
  "owner": "johndoe"
}
```

#### Retrieve Contact
```http
GET /api/contacts/1/
Authorization: Token your_token_here
```

#### Update Contact
```http
PUT /api/contacts/1/
Authorization: Token your_token_here
Content-Type: application/json

{
  "name": "Johnathan Doe",
  "email": "john.doe@example.com",
  "phone": "098-765-4321"
}
```

#### Partial Update Contact
```http
PATCH /api/contacts/1/
Authorization: Token your_token_here
Content-Type: application/json

{
  "phone": "111-222-3333"
}
```

#### Delete Contact
```http
DELETE /api/contacts/1/
Authorization: Token your_token_here
```

### Error Responses

#### Authentication Error (401)
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### Validation Error (400)
```json
{
  "email": ["Enter a valid email address."],
  "name": ["This field is required."]
}
```

#### Not Found (404)
```json
{
  "detail": "Not found."
}
```

### Data Validation Rules

| Field | Required | Validation Rules |
|-------|----------|------------------|
| name | Yes | Minimum 2 characters |
| email | Yes | Valid email format, no @example.com |
| phone | No | Digits only (after formatting), min 10 digits |

## 🎓 Educational Content

This project includes 8 comprehensive lessons that teach Django REST Framework development step by step:

### [Lesson 1: Django Project Setup](lessons/lesson-1-setup.md)
- Virtual environments and project initialization
- Django project vs app distinction
- Dependency management with requirements.txt

### [Lesson 2: Contact Model and Database](lessons/lesson-2-models.md)
- Django ORM and model definitions
- Database migrations and relationships
- Django admin interface setup

### [Lesson 3: DRF Serializers](lessons/lesson-3-serializers.md)
- Serialization and data validation
- ModelSerializer vs Serializer
- Custom validation methods

### [Lesson 4: DRF Views and ViewSets](lessons/lesson-4-views.md)
- ViewSets for automatic CRUD operations
- Custom permission classes
- Queryset filtering and user isolation

### [Lesson 5: URL Routing](lessons/lesson-5-urls.md)
- DRF routers and automatic URL generation
- Authentication endpoints
- URL configuration best practices

### [Lesson 6: Authentication Setup](lessons/lesson-6-auth.md)
- Token-based authentication
- Session authentication
- User isolation and security

### [Lesson 7: API Testing](lessons/lesson-7-testing.md)
- Comprehensive API testing with curl and Postman
- Testing authentication and authorization
- Error handling and validation testing

### [Lesson 8: Documentation and Next Steps](lessons/lesson-8-documentation.md)
- API documentation best practices
- Deployment considerations
- Extension ideas and next steps

### Bonus: [JWT Authentication](lessons/bonus-jwt-auth.md)
- JSON Web Tokens vs traditional authentication
- JWT implementation and configuration
- Advanced token management

## 🧪 Testing

### Quick Testing with curl

1. **Get authentication token**
   ```bash
   TOKEN=$(curl -s -X POST http://localhost:8000/api-token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}' \
     | jq -r .token)
   ```

2. **Test API endpoints**
   ```bash
   # List contacts
   curl -X GET http://localhost:8000/api/contacts/ \
     -H "Authorization: Token $TOKEN"

   # Create contact
   curl -X POST http://localhost:8000/api/contacts/ \
     -H "Authorization: Token $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test User", "email": "test@example.com"}'
   ```

### Django Test Framework

Run the built-in tests:
```bash
python manage.py test
```

### Test Coverage

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 🚀 Deployment

### Production Settings

1. **Update settings.py**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
   ```

2. **Environment Variables**
   ```bash
   export DJANGO_SECRET_KEY='your-secret-key'
   export DATABASE_URL='your-database-url'
   ```

3. **Database Setup**
   - Use PostgreSQL for production
   - Configure connection pooling
   - Set up read replicas if needed

4. **Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

### Deployment Options

#### Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn api_project.wsgi" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "api_project.wsgi:application"]
```

#### DigitalOcean/Render
- Use provided Django app templates
- Configure environment variables
- Set up automated deployments

### Security Considerations

- **HTTPS Only**: Always use HTTPS in production
- **Environment Variables**: Store sensitive data securely
- **Database Security**: Use strong passwords and connection encryption
- **Rate Limiting**: Implement request throttling
- **Regular Updates**: Keep dependencies updated

## 📈 Extension Ideas

### Immediate Enhancements
- **Pagination**: Handle large contact lists
- **Search**: Filter contacts by name or email
- **Sorting**: Order contacts by various fields
- **Export**: CSV or PDF export functionality

### Advanced Features
- **File Uploads**: Contact avatars
- **Bulk Operations**: Create/update multiple contacts
- **API Versioning**: Support multiple API versions
- **Real-time Updates**: WebSocket integration
- **Background Tasks**: Email notifications, data processing

### Integration Possibilities
- **Frontend Framework**: React, Vue.js, or Angular
- **Mobile App**: React Native or Flutter
- **Third-party Services**: Google Contacts sync
- **Analytics**: Usage tracking and reporting

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature-name
   ```
3. **Make your changes**
4. **Add tests for new functionality**
5. **Update documentation**
6. **Submit a pull request**

### Code Style

- Follow PEP 8 Python style guide
- Use descriptive variable names
- Add docstrings to functions and classes
- Write tests for new features
- Keep the code clean and readable

### Bug Reports

When reporting bugs, please include:
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages/logs

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework for perfectionists with deadlines
- [Django REST Framework](https://www.django-rest-framework.org/) - Powerful and flexible toolkit for building Web APIs
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/) - JSON Web Token authentication for DRF

## 📞 Support

If you have any questions or need help:

1. **Check the lessons**: Review the educational content
2. **Read the documentation**: Check API documentation
3. **Search issues**: Look for similar problems
4. **Create an issue**: Provide detailed information about your problem

## 🔗 Links

- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Documentation](https://www.django-rest-framework.org/)
- [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)
- [Python Packaging](https://packaging.python.org/)

---

**Happy Coding!** 🎉

This project was created to help developers learn Django REST Framework through practical, hands-on experience. Each concept is explained in detail with working examples and best practices.