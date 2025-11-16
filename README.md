# 🚀 Django REST Framework CRUD Demo

## 📋 Project Overview
This is a **beginner-friendly** Django REST Framework (DRF) project that demonstrates how to create a complete API with full CRUD (Create, Read, Update, Delete) operations. The project includes a User model and comprehensive API endpoints for managing user data.

## 🎯 Learning Objectives
By studying this project, beginners will learn:
- How Django models represent database tables
- How serializers convert between Python objects and JSON
- How views handle different HTTP methods (GET, POST, PUT, DELETE)
- How URL routing works in Django
- How to use Django's admin interface for data management
- How to build a complete REST API from scratch

## 📁 Project Structure
```
drfdemo/
├── manage.py              # Django's command-line utility
├── db.sqlite3            # SQLite database file
├── README.md             # This documentation file
├── drfdemo/              # Main project directory
│   ├── __init__.py       # Makes this a Python package
│   ├── settings.py       # Project configuration and settings
│   ├── urls.py          # Main URL routing configuration
│   ├── wsgi.py          # Web Server Gateway Interface
│   └── asgi.py          # Asynchronous Server Gateway Interface
└── api/                  # Your custom API application
    ├── __init__.py       # Makes this a Python package
    ├── models.py         # Database models (User model definition)
    ├── serializer.py     # Data serialization (JSON conversion)
    ├── views.py          # API logic (request handling)
    ├── urls.py           # API-specific URL patterns
    ├── admin.py          # Django admin configuration
    ├── apps.py           # App configuration
    ├── tests.py          # Test cases (for future testing)
    └── migrations/       # Database migration files
        ├── __init__.py
        └── 0001_initial.py
```

## 🔧 Key Components Explained

### 1. 📊 Models (`api/models.py`)
**What it does**: Defines the structure of your database tables using Python classes.

```python
class User(models.Model):
    name = models.CharField(max_length=100)  # Text field for user's name
    age = models.IntegerField()              # Number field for user's age
```

**Key Concepts**:
- Each model class = one database table
- Each field = one column in the table
- Django automatically creates an `id` field as primary key
- `__str__` method controls how objects are displayed

### 2. 🔄 Serializers (`api/serializer.py`)
**What it does**: Acts as a translator between Python objects and JSON data.

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
```

**Key Concepts**:
- Converts User objects → JSON (for API responses)
- Converts JSON → User objects (for API requests)
- Handles data validation automatically
- `ModelSerializer` creates fields based on the model

### 3. 🎮 Views (`api/views.py`)
**What it does**: Contains the logic for handling different HTTP requests.

#### Available Endpoints:

1. **Get All Users** (`GET /api/users/`)
   ```python
   @api_view(['GET'])
   def get_users(request):
       users = User.objects.all()           # Fetch all users
       serializer = UserSerializer(users, many=True)  # Convert to JSON
       return Response(serializer.data)     # Return as response
   ```

2. **Create User** (`POST /api/users/create`)
   ```python
   @api_view(['POST'])
   def create_user(request):
       serializer = UserSerializer(data=request.data)  # Create serializer with request data
       if serializer.is_valid():            # Validate the data
           serializer.save()                # Save to database
           return Response(serializer.data, status=201)  # Return created user
       return Response(serializer.errors, status=400)   # Return validation errors
   ```

3. **User Detail Operations** (`GET/PUT/DELETE /api/users/<id>/`)
   ```python
   @api_view(['GET', 'PUT', 'DELETE'])
   def user_detail(request, user_id):
       user = User.objects.get(id=user_id)  # Find specific user
       
       if request.method == 'GET':          # Read user data
           # Return user information
       elif request.method == 'PUT':        # Update user data
           # Update and return modified user
       elif request.method == 'DELETE':     # Delete user
           # Remove user from database
   ```

### 4. 🗺️ URL Routing (`urls.py` files)
**What it does**: Maps URLs to view functions.

#### Main URLs (`drfdemo/urls.py`):
```python
urlpatterns = [
    path('admin/', admin.site.urls),     # Django admin interface
    path('api/', include('api.urls')),   # Include API app URLs
]
```

#### API URLs (`api/urls.py`):
```python
urlpatterns = [
    path('users/', get_users, name='get_users'),                    # List all users
    path('users/create/', create_user, name='create_user'),         # Create new user
    path('users/<int:user_id>/', user_detail, name='user_detail'), # Individual user operations
]
```

### 5. ⚙️ Admin Interface (`api/admin.py`)
**What it does**: Provides a web-based interface for managing data.

```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age']    # Columns to show in list view
    search_fields = ['name']                 # Enable search by name
    list_filter = ['age']                    # Add age filter sidebar
```

## 🚀 Getting Started

### Prerequisites
- Python 3.x installed
- Basic understanding of Python
- Text editor or IDE (VS Code recommended)

### Installation & Setup

1. **Navigate to the project directory**:
   ```bash
   cd drfdemo
   ```

2. **Apply database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create a superuser (for admin access)**:
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

4. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the application**:
   - API: `http://127.0.0.1:8000/api/users/`
   - Admin: `http://127.0.0.1:8000/admin/`

## 🌐 API Endpoints Reference

| Method | URL | Description | Example Request Body |
|--------|-----|-------------|---------------------|
| GET | `/api/users/` | Get all users | None |
| POST | `/api/users/create` | Create new user | `{"name": "John Doe", "age": 30}` |
| GET | `/api/users/1/` | Get user by ID | None |
| PUT | `/api/users/1/` | Update user | `{"name": "Jane Doe", "age": 31}` |
| DELETE | `/api/users/1/` | Delete user | None |

### Example API Usage

#### 1. Create a New User
```bash
curl -X POST http://127.0.0.1:8000/api/users/create \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Johnson", "age": 28}'
```

#### 2. Get All Users
```bash
curl http://127.0.0.1:8000/api/users/
```

#### 3. Update a User
```bash
curl -X PUT http://127.0.0.1:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Smith", "age": 29}'
```

#### 4. Delete a User
```bash
curl -X DELETE http://127.0.0.1:8000/api/users/1/
```

## 🎓 Learning Path for Beginners

### Phase 1: Understanding the Basics
1. **Study Models** (`api/models.py`)
   - Learn how Python classes represent database tables
   - Understand different field types (`CharField`, `IntegerField`)
   - Practice adding new fields to the User model

2. **Explore Serializers** (`api/serializer.py`)
   - Understand the role of serializers in API development
   - Learn about `ModelSerializer` vs `Serializer`
   - Practice customizing serializer fields

### Phase 2: API Development
3. **Master Views** (`api/views.py`)
   - Learn how `@api_view` decorator works
   - Understand HTTP methods (GET, POST, PUT, DELETE)
   - Practice error handling and validation

4. **URL Routing** (`urls.py` files)
   - Learn how Django routes URLs to views
   - Understand URL parameters (`<int:user_id>`)
   - Practice creating new URL patterns

### Phase 3: Administration
5. **Admin Interface** (`api/admin.py`)
   - Learn how to register models
   - Customize admin views
   - Use admin for data management

### Phase 4: Testing and Enhancement
6. **Testing Your API**
   - Use Django REST Framework's browsable API
   - Test with tools like Postman or curl
   - Write basic unit tests

## 🔨 Next Steps for Development

### Immediate Enhancements
1. **Add Data Validation**
   - Add minimum/maximum age constraints
   - Validate name format (no numbers, minimum length)
   - Add email field with email validation

2. **Improve Error Handling**
   - Add custom error messages
   - Handle edge cases (empty requests, invalid IDs)
   - Add logging for debugging

3. **Add More Fields**
   ```python
   class User(models.Model):
       name = models.CharField(max_length=100)
       age = models.IntegerField()
       email = models.EmailField(unique=True)  # New field
       created_at = models.DateTimeField(auto_now_add=True)  # New field
   ```

### Advanced Features
4. **Authentication & Permissions**
   - Add user authentication
   - Implement API permissions
   - Add user roles and access control

5. **Advanced Querying**
   - Add search and filtering
   - Implement pagination
   - Add sorting options

6. **API Documentation**
   - Add Swagger/OpenAPI documentation
   - Create detailed API guides
   - Add example requests/responses

## 🛠️ Common Tasks

### Adding a New Field to User Model
1. Update the model in `models.py`
2. Create and apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Update admin configuration if needed

### Creating a New Model
1. Add the model class to `models.py`
2. Create a serializer for it in `serializer.py`
3. Add views in `views.py`
4. Configure URLs in `urls.py`
5. Register in admin (optional)

### Testing Your Changes
1. Use Django's browsable API: `http://127.0.0.1:8000/api/users/`
2. Test with curl commands (examples above)
3. Use the Django admin interface
4. Write unit tests in `tests.py`

## 🆘 Troubleshooting

### Common Issues
1. **"No module named 'rest_framework'"**
   - Install Django REST Framework: `pip install djangorestframework`

2. **"Table doesn't exist" errors**
   - Run migrations: `python manage.py migrate`

3. **"Permission denied" in admin**
   - Create superuser: `python manage.py createsuperuser`

4. **Changes not appearing**
   - Restart the development server
   - Clear browser cache
   - Check for syntax errors in Python files

## 📚 Additional Resources

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Django Model Field Reference](https://docs.djangoproject.com/en/stable/ref/models/fields/)

### Tutorials
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)
- [Django REST Framework Tutorial](https://www.django-rest-framework.org/tutorial/1-serialization/)
- [Real Python Django Tutorials](https://realpython.com/tutorials/django/)

### Tools
- [Postman](https://www.postman.com/) - API testing tool
- [DB Browser for SQLite](https://sqlitebrowser.org/) - Database viewer
- [VS Code REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) - VS Code extension for API testing

## ❓ Frequently Asked Questions

**Q: What's the difference between Django and Django REST Framework?**
A: Django is a web framework for building websites, while Django REST Framework (DRF) is an extension that makes it easy to build Web APIs.

**Q: Why use serializers instead of returning model objects directly?**
A: Serializers provide data validation, format conversion (Python ↔ JSON), and security by controlling which fields are exposed.

**Q: What happens when I visit `/api/users/`?**
A: Django matches the URL pattern, calls the `get_users` view function, which fetches users from the database and returns them as JSON.

**Q: How do I add authentication to my API?**
A: Django REST Framework provides multiple authentication options. Start with the built-in `SessionAuthentication` or `TokenAuthentication`.

**Q: Can I use a different database than SQLite?**
A: Yes! Django supports PostgreSQL, MySQL, SQLite, and Oracle. Change the database configuration in `settings.py`.
