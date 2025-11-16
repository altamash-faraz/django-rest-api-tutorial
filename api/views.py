# Import Django's render function (used for rendering HTML templates)
from django.shortcuts import render

# Create your views here.
# Views handle HTTP requests and return HTTP responses

# Import Django REST Framework components
from rest_framework.decorators import api_view  # Decorator to create API views
from rest_framework.response import Response    # Special response class for API responses
from rest_framework import status              # HTTP status codes (200, 404, 500, etc.)

# Import our models and serializers
from .models import User           # Our User model
from .serializer import UserSerializer  # Our User serializer

# @api_view is a decorator that converts a regular function into a REST API view
# ['GET'] means this view only accepts GET requests (for retrieving data)
# Other HTTP methods include: POST (create), PUT (update), DELETE (remove)
@api_view(['GET'])
def get_users(request):
    """
    API endpoint that returns all users from the database.
    
    This function handles GET requests to retrieve all user records.
    Unlike the original hardcoded example, this fetches real data from the database.
    
    Args:
        request: The HTTP request object containing information about the request
        
    Returns:
        Response: A JSON response containing a list of all users
        
    Example response:
    [
        {"id": 1, "name": "John Doe", "age": 30},
        {"id": 2, "name": "Alice Smith", "age": 25}
    ]
    """
    
    # Fetch all User objects from the database
    # User.objects.all() returns a QuerySet containing all user records
    users = User.objects.all()
    
    # Serialize the QuerySet to convert Python objects to JSON-friendly format
    # many=True tells the serializer that we're passing multiple objects (a list)
    # Without many=True, it would expect a single User instance
    serializer = UserSerializer(users, many=True)
    
    # Return the serialized data as a JSON response
    # .data converts the serialized objects to Python dictionaries/lists
    return Response(serializer.data)


@api_view(['POST'])
def create_user(request):
    """
    API endpoint to create a new user.
    
    This function handles POST requests to create new user records in the database.
    It expects JSON data containing 'name' and 'age' fields.
    
    Args:
        request: The HTTP request object containing user data in request.data
        
    Returns:
        Response: 
        - 201 Created with user data if successful
        - 400 Bad Request with error details if validation fails
        
    Example request data:
    {
        "name": "Alice Smith", 
        "age": 25
    }
    """
    
    # Create a serializer instance with the data from the request
    # request.data contains the JSON data sent by the client
    serializer = UserSerializer(data=request.data)
    
    # Check if the provided data is valid according to our model rules
    # This validates field types, required fields, max lengths, etc.
    if serializer.is_valid():
        # If data is valid, save the new user to the database
        # .save() creates a new User record and returns the instance
        serializer.save()
        
        # Return the created user data with HTTP 201 (Created) status
        # This tells the client the resource was successfully created
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # If validation failed, return the errors with HTTP 400 (Bad Request)
    # serializer.errors contains details about what went wrong
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## CRUD Operations - Complete Create, Read, Update, Delete functionality

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, user_id):
    """
    API endpoint to handle individual user operations.
    
    This function handles three different HTTP methods for a specific user:
    - GET: Retrieve user details
    - PUT: Update user information  
    - DELETE: Remove user from database
    
    Args:
        request: The HTTP request object
        user_id: The ID of the user to operate on (extracted from URL)
        
    Returns:
        Response: Different responses based on the HTTP method used
        
    URL pattern: /api/users/1/ (where 1 is the user_id)
    """
    
    try:
        # Try to find the user with the given ID in the database
        # User.objects.get() raises an exception if user doesn't exist
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # If user doesn't exist, return HTTP 404 (Not Found)
        # This is a standard response when a resource cannot be found
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Handle different HTTP methods using if-elif-else structure
    
    if request.method == 'GET':
        """
        GET request: Return user information
        Used when client wants to retrieve details of a specific user
        """
        # Convert the user object to JSON format using our serializer
        serializer = UserSerializer(user)
        # Return the user data as JSON response
        return Response(serializer.data)

    elif request.method == 'PUT':
        """
        PUT request: Update user information
        Used when client wants to modify existing user data
        Expects JSON data with fields to update
        """
        # Create serializer with existing user instance and new data
        # This tells Django to update the existing user rather than create new one
        serializer = UserSerializer(user, data=request.data)
        
        # Validate the new data
        if serializer.is_valid():
            # If valid, save the changes to the database
            serializer.save()
            # Return the updated user data
            return Response(serializer.data)
        
        # If validation failed, return error details
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        """
        DELETE request: Remove user from database
        Used when client wants to permanently delete a user
        """
        # Delete the user from the database
        # This permanently removes the record
        user.delete()
        
        # Return HTTP 204 (No Content) - successful deletion with no response body
        # This is the standard response for successful DELETE operations
        return Response(status=status.HTTP_204_NO_CONTENT)