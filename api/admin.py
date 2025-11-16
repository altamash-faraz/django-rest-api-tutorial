# Import Django's admin module for creating admin interface
from django.contrib import admin

# Import our User model to register it with the admin
from .models import User

# Register your models here.
# This makes the User model available in the Django admin interface

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin configuration for the User model.
    
    This class customizes how the User model appears in the Django admin interface.
    It makes it easier for administrators to manage user data through a web interface.
    """
    
    # Fields to display in the admin list view (when viewing all users)
    # This shows a table with these columns
    list_display = ['id', 'name', 'age']
    
    # Fields that can be clicked to view/edit the individual record
    list_display_links = ['id', 'name']
    
    # Add search functionality to find users by name
    # This adds a search box at the top of the admin page
    search_fields = ['name']
    
    # Add filtering options in the right sidebar
    # Users can filter by age ranges
    list_filter = ['age']
    
    # Set ordering for the list view (newest first by ID)
    ordering = ['-id']
    
    # Fields to display when creating/editing a user
    # This defines the form layout
    fields = ['name', 'age']
    
# Alternative way to register (if you prefer the simpler approach):
# admin.site.register(User)

# Benefits of registering models in admin:
# 1. Easy data management through web interface
# 2. No need to write custom forms for basic CRUD operations
# 3. Built-in user authentication and permissions
# 4. Quick way to add/edit/delete records during development
# 5. Useful for content management and testing
