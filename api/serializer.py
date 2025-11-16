# Import Django REST Framework's serializers
# Serializers convert complex data types (like Django model instances) to 
# native Python data types that can then be easily rendered into JSON
from rest_framework import serializers

# Import our User model from the current app
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer converts User model instances to/from JSON.
    
    Think of a serializer as a translator:
    - It translates Python objects (User instances) to JSON (for API responses)
    - It translates JSON data (from API requests) to Python objects
    
    ModelSerializer is a special type that automatically creates serializer fields
    based on the model fields, making our code shorter and easier to maintain.
    """
    
    class Meta:
        """
        Meta class provides metadata about the serializer.
        It tells Django REST Framework how to configure this serializer.
        """
        
        # Specify which model this serializer is for
        model = User
        
        # '__all__' means include ALL fields from the User model
        # This will automatically include 'id', 'age', and 'name' fields
        # Alternative: fields = ['id', 'name', 'age'] to specify exact fields
        fields = '__all__'