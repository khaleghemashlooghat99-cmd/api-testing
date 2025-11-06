# Lesson 1: Django Project Setup

## Learning Goals
- Understand what virtual environments are and why they matter
- Learn the difference between Django projects and apps
- Set up a complete Django REST Framework development environment
- Understand Django's project structure

## What is a Virtual Environment?

A virtual environment is an isolated Python environment that allows you to:
- Keep project dependencies separate from other projects
- Use different versions of packages for different projects
- Avoid conflicts between package dependencies
- Create reproducible development environments

## Step-by-Step Setup

### 1. Create Virtual Environment
```bash
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

**What this does:**
- Creates a `venv/` directory with isolated Python installation
- Copies Python executable and essential packages
- Sets up paths for isolated package management

### 2. Install Dependencies
```bash
# Install all required packages from requirements.txt
pip install -r requirements.txt
```

**Our Dependencies Explained:**
- **django==4.2.7**: Django web framework (LTS version for stability)
- **djangorestframework==3.14.0**: REST API toolkit for Django
- **djangorestframework-simplejwt==5.3.0**: JWT authentication (bonus lesson)

### 3. Create Django Project
```bash
# Create a Django project (the . means current directory)
django-admin startproject api_project .
```

**What this creates:**
- `api_project/`: Project configuration directory
- `manage.py`: Django's command-line utility
- Database configuration and settings

### 4. Create Django App
```bash
# Create a Django app for our contacts functionality
python manage.py startapp contacts
```

**What this creates:**
- `contacts/`: App directory with models, views, templates, etc.
- Each app handles a specific piece of functionality
- Apps are reusable components

## Understanding Django's Structure

### Project vs App
- **Project**: Collection of settings and apps (configuration level)
- **App**: Web application that does something (functional level)
- A project can contain multiple apps
- Apps can be used in multiple projects

### Key Files Created
- `manage.py`: Django management script
- `api_project/settings.py`: All Django configuration
- `api_project/urls.py`: URL routing configuration
- `contacts/models.py`: Database models
- `contacts/views.py`: Web page/API views
- `contacts/admin.py`: Django admin configuration

## Common Commands
```bash
# Run development server
python manage.py runserver

# Create migrations from model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Open Django shell for testing
python manage.py shell
```

## Key Concepts Covered

### Virtual Environments
- **Why**: Dependency isolation and reproducibility
- **How**: `python -m venv venv` and `source venv/bin/activate`
- **Best Practice**: Always use virtual environments for Python projects

### Django Projects vs Apps
- **Project**: Configuration and settings
- **App**: Functional components
- **Relationship**: Projects contain apps, apps can be reused

### Package Management
- **requirements.txt**: Lists all project dependencies
- **Pip**: Python package manager
- **Version Pinning**: Use specific versions for stability

## Success Criteria
- [ ] Virtual environment created and activated
- [ ] All dependencies installed without errors
- [ ] Django project created successfully
- [ ] Django app created successfully
- [ ] Development server runs without errors (`python manage.py runserver`)

## Troubleshooting

### Common Issues
1. **Virtual environment won't activate**
   - Make sure you're using the right path for your OS
   - Check that Python is installed correctly

2. **Pip install fails**
   - Try upgrading pip: `pip install --upgrade pip`
   - Check Python version compatibility

3. **Django project creation fails**
   - Make sure virtual environment is active
   - Check that Django was installed successfully

4. **Port already in use**
   - Use different port: `python manage.py runserver 8001`

## Next Steps
In the next lesson, we'll create our Contact model and learn about Django's ORM and database migrations.

## Additional Resources
- [Django Official Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Python Virtual Environments](https://docs.python.org/3/library/venv.html)
- [Django REST Framework Quickstart](https://www.django-rest-framework.org/tutorial/quickstart/)