# Import Django's URL routing functions
from django.urls import path

# Import views from the current app
# The dot (.) means "from the current directory/app"
from .views import create_user, get_users, user_detail

# URL patterns define which URLs map to which views
# This is like a phone book: when someone visits a URL, Django looks here
# to find which view function should handle the request

urlpatterns = [
    # URL PATTERN STRUCTURE: path('url-pattern/', view_function, name='url-name')
    
    # 1. GET ALL USERS - List endpoint
    # 'users/' - When someone visits /api/users/ (GET request)
    # get_users - The view function that handles fetching all users from database
    # name='get_users' - A unique name for this URL pattern (useful for reversing URLs)
    path('users/', get_users, name='get_users'),
    
    # 2. CREATE NEW USER - Create endpoint  
    # 'users/create' - When someone visits /api/users/create (POST request)
    # create_user - The view function that handles creating new users
    # Expects JSON data like: {"name": "John Doe", "age": 30}
    path('users/create', create_user, name='create_user'),
    
    # 3. INDIVIDUAL USER OPERATIONS - Detail endpoint with URL parameter
    # 'users/<int:user_id>/' - Dynamic URL that captures user ID as integer
    # Examples: /api/users/1/, /api/users/25/, /api/users/100/
    # user_detail - The view function that handles GET/PUT/DELETE for specific users
    # <int:user_id> - URL parameter that gets passed to the view function
    path('users/<int:user_id>/', user_detail, name='user_detail'),
    
    # COMPLETE API ENDPOINTS SUMMARY:
    # GET    /api/users/           → get_users()     → List all users
    # POST   /api/users/create     → create_user()   → Create new user  
    # GET    /api/users/1/         → user_detail()   → Get user #1 details
    # PUT    /api/users/1/         → user_detail()   → Update user #1
    # DELETE /api/users/1/         → user_detail()   → Delete user #1
    
    # How URL parameters work:
    # - <int:user_id> captures an integer from the URL
    # - The captured value is passed as an argument to the view function
    # - Example: /api/users/5/ calls user_detail(request, user_id=5)
    
    # Future URL patterns you might add:
    # path('users/search/', search_users, name='search_users'),           # Search functionality
    # path('users/<int:user_id>/avatar/', user_avatar, name='user_avatar'), # Profile pictures
    # path('users/stats/', user_statistics, name='user_stats'),           # User statistics
]