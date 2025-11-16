# Import Django's models module to create database models
from django.db import models

# Create your models here.
# Models define the structure of your database tables

class User(models.Model):
    """
    User model represents a user in our application.
    This class inherits from Django's Model class, which provides
    all the functionality for database operations (create, read, update, delete).
    """
    
    # IntegerField creates a column in the database that stores whole numbers
    # This will store the user's age as an integer (e.g., 25, 30, 45)
    age = models.IntegerField()
    
    # CharField creates a column that stores text/strings
    # max_length=100 means the name can be up to 100 characters long
    # This will store the user's name as text (e.g., "John Doe", "Alice Smith")
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        This special method defines what gets displayed when you print a User object.
        Instead of showing something like "<User object (1)>", it will show the user's name.
        This is very helpful in the Django admin interface and when debugging.
        """
        return self.name
    
