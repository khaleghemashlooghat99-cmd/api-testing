# Lesson 2: Contact Model and Database

## Learning Goals
- Understand Django's ORM (Object-Relational Mapper)
- Learn how to define database models
- Create and run database migrations
- Set up Django admin interface
- Understand model relationships and fields

## What is Django ORM?

Django ORM is a powerful feature that allows you to:
- Define database tables using Python classes
- Query databases using Python methods instead of SQL
- Handle database relationships using Python objects
- Switch databases without changing your Python code

## Our Contact Model

Let's examine our Contact model in `contacts/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'email']

    def __str__(self):
        return f"{self.name} ({self.email})"
```

## Model Field Types Explained

### owner (ForeignKey)
```python
owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
```
- **ForeignKey**: Creates a many-to-one relationship
- **User**: References Django's built-in User model
- **on_delete=models.CASCADE**: If user is deleted, delete their contacts too
- **related_name='contacts'**: Allows us to do `user.contacts.all()`

### name (CharField)
```python
name = models.CharField(max_length=100)
```
- **CharField**: For short text strings
- **max_length=100**: Maximum 100 characters
- **Required field** (no `blank=True`)

### email (EmailField)
```python
email = models.EmailField()
```
- **EmailField**: Special CharField that validates email format
- **Required field** (no `blank=True`)

### phone (CharField)
```python
phone = models.CharField(max_length=20, blank=True)
```
- **CharField**: We use CharField instead of IntegerField for phone numbers
- **blank=True**: This field is optional
- **Why not IntegerField?**: Phone numbers can contain +, -, (, ), spaces

### Timestamp Fields
```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```
- **DateTimeField**: Stores date and time
- **auto_now_add=True**: Set only when object is first created
- **auto_now=True**: Updated every time object is saved

## Model Meta Options

```python
class Meta:
    ordering = ['-created_at']        # Default ordering: newest first
    unique_together = ['owner', 'email']  # Prevent duplicate emails per user
```

### Common Meta Options
- **ordering**: Default query ordering
- **verbose_name**: Human-readable model name
- **verbose_name_plural**: Plural version
- **db_table**: Custom table name
- **unique_together**: Multiple-field uniqueness constraints

## Model Methods

```python
def __str__(self):
    return f"{self.name} ({self.email})"
```
- **__str__**: Human-readable string representation
- Used in Django admin and debugging
- Should be descriptive but concise

## Database Migrations

### What are Migrations?
Migrations are Django's way of:
- Propagating changes to your database schema
- Keeping track of model changes over time
- Allowing rollback to previous versions
- Enabling team collaboration

### Creating Migrations
```bash
python manage.py makemigrations
```
This command:
- Scans all models in installed apps
- Compares with current migration files
- Creates new migration file for changes
- Shows what changes will be made

### Applying Migrations
```bash
python manage.py migrate
```
This command:
- Applies any unapplied migrations
- Creates database tables
- Alters existing table structures
- Updates database schema

### Migration Files
Located in `contacts/migrations/`:
- `0001_initial.py`: Creates Contact table
- Future migrations: Add/remove fields, change constraints

## Django Admin Setup

### Why Use Django Admin?
- Automatically generated CRUD interface
- Perfect for development and testing
- Easy data management without coding
- Customizable and extensible

### Our Admin Configuration
```python
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'owner')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
```

### Admin Options Explained
- **list_display**: Columns shown in list view
- **list_filter**: Right sidebar filters
- **search_fields**: Enable search functionality
- **readonly_fields**: Fields that can't be edited
- **ordering**: Default ordering in admin

## Creating a Superuser

```bash
python manage.py createsuperuser
```
Follow prompts to create admin credentials:
- Username: Choose something memorable
- Email: Your email address
- Password: Choose a strong password

## Testing the Model

### Django Shell
```bash
python manage.py shell
```

### Basic Model Operations
```python
# Import models
from contacts.models import Contact
from django.contrib.auth.models import User

# Get or create a user
user = User.objects.create_user('testuser', 'test@example.com', 'password123')

# Create a contact
contact = Contact.objects.create(
    owner=user,
    name='John Doe',
    email='john@example.com',
    phone='123-456-7890'
)

# Query contacts
contacts = Contact.objects.filter(owner=user)
print(contacts)

# Update a contact
contact.phone = '098-765-4321'
contact.save()

# Delete a contact
contact.delete()
```

## Key Concepts Covered

### Django ORM
- **Models as Python classes**: Database tables as Python objects
- **Fields as class attributes**: Table columns as class attributes
- **QuerySets**: Database queries return Python objects
- **No SQL needed**: Django writes SQL for you

### Database Relationships
- **ForeignKey**: Many-to-one relationships
- **ManyToMany**: Many-to-many relationships
- **OneToOne**: One-to-one relationships

### Migrations
- **Model to Database**: Sync Python models with database
- **Version Control**: Track schema changes over time
- **Team Collaboration**: Consistent database structure

## Success Criteria
- [ ] Contact model created with all required fields
- [ ] Migrations created successfully
- [ ] Database updated without errors
- [ ] Superuser created
- [ ] Django admin accessible and working
- [ ] Can create/view contacts in admin interface

## Common Issues

### Migration Problems
1. **Migration conflicts**: Use `python manage.py migrate --fake`
2. **Database locked**: Stop the development server and try again
3. **SQLite file missing**: Run `python manage.py migrate` to create it

### Model Issues
1. **Field name collisions**: Avoid Django reserved words
2. **Relationship errors**: Make sure related models exist
3. **Validation errors**: Check field constraints

## Next Steps
In the next lesson, we'll create DRF serializers to convert our Contact model data to/from JSON format.

## Additional Resources
- [Django Models Documentation](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Migrations](https://docs.djangoproject.com/en/stable/topics/migrations/)
- [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)