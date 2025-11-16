# Import Django testing framework
from django.test import TestCase

# Import Django REST Framework testing tools
from rest_framework.test import APITestCase
from rest_framework import status

# Import our models and serializers
from .models import User
from .serializer import UserSerializer

# Create your tests here.
# Tests help ensure your code works correctly and prevent bugs

class UserModelTest(TestCase):
    """
    Test cases for the User model.
    
    These tests verify that the User model works correctly:
    - Creating users
    - String representation (__str__ method)
    - Field validation
    """
    
    def setUp(self):
        """
        Set up test data before each test method runs.
        This method is called before every test function.
        """
        # Create a test user for use in tests
        self.user = User.objects.create(name="Test User", age=25)
    
    def test_user_creation(self):
        """Test that a user can be created successfully."""
        # Verify the user was created with correct attributes
        self.assertEqual(self.user.name, "Test User")
        self.assertEqual(self.user.age, 25)
        self.assertTrue(self.user.id)  # Ensure ID was assigned
    
    def test_user_str_representation(self):
        """Test the string representation of a user (__str__ method)."""
        # The __str__ method should return the user's name
        self.assertEqual(str(self.user), "Test User")
    
    def test_user_fields(self):
        """Test that user fields are properly configured."""
        # Get the model's field information
        name_field = User._meta.get_field('name')
        age_field = User._meta.get_field('age')
        
        # Verify field properties
        self.assertEqual(name_field.max_length, 100)
        self.assertEqual(age_field.__class__.__name__, 'IntegerField')


class UserSerializerTest(TestCase):
    """
    Test cases for the UserSerializer.
    
    These tests verify that the serializer correctly:
    - Converts model instances to JSON
    - Validates input data
    - Creates new instances from data
    """
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create(name="Serializer Test User", age=30)
        self.valid_data = {"name": "New User", "age": 22}
        self.invalid_data = {"name": "", "age": "not_a_number"}
    
    def test_user_serialization(self):
        """Test converting a User instance to JSON data."""
        serializer = UserSerializer(self.user)
        expected_data = {
            'id': self.user.id,
            'name': 'Serializer Test User',
            'age': 30
        }
        self.assertEqual(serializer.data, expected_data)
    
    def test_valid_user_deserialization(self):
        """Test creating a User from valid JSON data."""
        serializer = UserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.name, "New User")
        self.assertEqual(user.age, 22)
    
    def test_invalid_user_deserialization(self):
        """Test that invalid data is properly rejected."""
        serializer = UserSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('age', serializer.errors)  # Age should have validation error


class UserAPITest(APITestCase):
    """
    Test cases for the User API endpoints.
    
    These tests verify that the API endpoints work correctly:
    - GET requests return proper data
    - POST requests create new users
    - PUT requests update existing users
    - DELETE requests remove users
    - Error handling works properly
    """
    
    def setUp(self):
        """Set up test data and URLs."""
        # Create test users
        self.user1 = User.objects.create(name="API Test User 1", age=25)
        self.user2 = User.objects.create(name="API Test User 2", age=35)
        
        # Define API URLs for testing
        self.users_url = '/api/users/'
        self.create_url = '/api/users/create'
        self.detail_url = f'/api/users/{self.user1.id}/'
    
    def test_get_users_list(self):
        """Test GET /api/users/ - should return all users."""
        response = self.client.get(self.users_url)
        
        # Verify response status and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 users
        
        # Verify user data is included
        user_names = [user['name'] for user in response.data]
        self.assertIn("API Test User 1", user_names)
        self.assertIn("API Test User 2", user_names)
    
    def test_create_user(self):
        """Test POST /api/users/create - should create a new user."""
        new_user_data = {"name": "Created User", "age": 28}
        response = self.client.post(self.create_url, new_user_data, format='json')
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Created User")
        self.assertEqual(response.data['age'], 28)
        
        # Verify user was actually created in database
        self.assertTrue(User.objects.filter(name="Created User").exists())
    
    def test_create_user_invalid_data(self):
        """Test POST with invalid data - should return validation errors."""
        invalid_data = {"name": "", "age": "invalid"}
        response = self.client.post(self.create_url, invalid_data, format='json')
        
        # Should return 400 Bad Request with validation errors
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)  # Name field error
        self.assertIn('age', response.data)   # Age field error
    
    def test_get_user_detail(self):
        """Test GET /api/users/1/ - should return specific user."""
        response = self.client.get(self.detail_url)
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user1.id)
        self.assertEqual(response.data['name'], "API Test User 1")
    
    def test_update_user(self):
        """Test PUT /api/users/1/ - should update existing user."""
        update_data = {"name": "Updated User", "age": 26}
        response = self.client.put(self.detail_url, update_data, format='json')
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated User")
        self.assertEqual(response.data['age'], 26)
        
        # Verify database was updated
        updated_user = User.objects.get(id=self.user1.id)
        self.assertEqual(updated_user.name, "Updated User")
        self.assertEqual(updated_user.age, 26)
    
    def test_delete_user(self):
        """Test DELETE /api/users/1/ - should remove user."""
        response = self.client.delete(self.detail_url)
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify user was deleted from database
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())
    
    def test_user_not_found(self):
        """Test accessing non-existent user - should return 404."""
        non_existent_url = '/api/users/99999/'
        response = self.client.get(non_existent_url)
        
        # Should return 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# How to run these tests:
# 1. In terminal: python manage.py test
# 2. To run specific test class: python manage.py test api.tests.UserModelTest
# 3. To run with verbose output: python manage.py test --verbosity=2
# 4. To run and see test coverage: pip install coverage, then:
#    coverage run --source='.' manage.py test
#    coverage report

# Why testing is important:
# 1. Ensures your code works as expected
# 2. Catches bugs early in development
# 3. Makes refactoring safer
# 4. Provides documentation of expected behavior
# 5. Builds confidence when making changes
