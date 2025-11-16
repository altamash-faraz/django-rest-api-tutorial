"""
URL configuration for drfdemo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Import Django's admin interface and URL routing functions
from django.contrib import admin
from django.urls import path, include

# Main URL configuration for the entire project
# This is the ROOT URL configuration that Django checks first

urlpatterns = [
    # Django Admin Interface
    # When someone visits /admin/, they'll see Django's built-in admin panel
    # This is where you can manage users, view database records, etc.
    path('admin/', admin.site.urls),
    
    # API URLs - Include all URLs from our 'api' app
    # include() tells Django to look in the api/urls.py file for more URL patterns
    # This means:
    # - /api/users/ will be handled by the get_user view in api/views.py
    # - Any new URLs added to api/urls.py will automatically work under /api/
    path('api/', include('api.urls')),
    
    # Example: If you had a blog app, you might add:
    # path('blog/', include('blog.urls')),
]
