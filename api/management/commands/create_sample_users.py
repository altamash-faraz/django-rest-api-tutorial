# Import Django's base command class
from django.core.management.base import BaseCommand

# Import our User model
from api.models import User


class Command(BaseCommand):
    """
    Django management command to create sample user data.
    
    This command provides an easy way to populate the database with sample users
    for testing and demonstration purposes.
    
    Usage:
        python manage.py create_sample_users
        
    This is helpful for:
    - Testing API endpoints with real data
    - Demonstrating the application to others
    - Setting up development environments quickly
    """
    
    # Help text displayed when running: python manage.py help create_sample_users
    help = 'Create sample user data for testing and demonstration'

    def add_arguments(self, parser):
        """
        Add command-line arguments to the management command.
        
        Args:
            parser: The argument parser instance
        """
        # Optional argument to specify number of users to create
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of sample users to create (default: 5)',
        )
        
        # Optional flag to clear existing users before creating new ones
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing users before creating sample data',
        )

    def handle(self, *args, **options):
        """
        Main command execution logic.
        
        This method is called when the command is executed.
        It contains the actual code that creates sample users.
        
        Args:
            *args: Positional arguments
            **options: Command-line options and arguments
        """
        
        # Get command options
        count = options['count']
        clear_existing = options['clear']
        
        # Clear existing users if requested
        if clear_existing:
            deleted_count = User.objects.count()
            User.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'Deleted {deleted_count} existing users')
            )
        
        # Sample user data - realistic names and ages
        sample_users = [
            {'name': 'Alice Johnson', 'age': 28},
            {'name': 'Bob Smith', 'age': 35},
            {'name': 'Charlie Brown', 'age': 22},
            {'name': 'Diana Prince', 'age': 30},
            {'name': 'Edward Wilson', 'age': 45},
            {'name': 'Fiona Davis', 'age': 26},
            {'name': 'George Miller', 'age': 33},
            {'name': 'Hannah Taylor', 'age': 29},
            {'name': 'Ian Anderson', 'age': 41},
            {'name': 'Julia Roberts', 'age': 37},
        ]
        
        # Create users up to the requested count
        created_count = 0
        for i in range(min(count, len(sample_users))):
            user_data = sample_users[i]
            
            # Check if user with this name already exists
            if not User.objects.filter(name=user_data['name']).exists():
                # Create the user
                user = User.objects.create(
                    name=user_data['name'],
                    age=user_data['age']
                )
                created_count += 1
                
                # Output progress with colored text
                self.stdout.write(
                    f'Created user: {user.name} (age {user.age})'
                )
            else:
                # User already exists, skip
                self.stdout.write(
                    self.style.WARNING(
                        f'User "{user_data["name"]}" already exists, skipping'
                    )
                )
        
        # If more users requested than we have sample data for
        if count > len(sample_users):
            # Create additional users with generated names
            for i in range(len(sample_users), count):
                user_name = f'Sample User {i + 1}'
                user_age = 20 + (i % 30)  # Ages between 20-49
                
                if not User.objects.filter(name=user_name).exists():
                    user = User.objects.create(name=user_name, age=user_age)
                    created_count += 1
                    self.stdout.write(f'Created user: {user.name} (age {user.age})')
        
        # Final summary message
        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {created_count} sample users!'
                )
            )
            self.stdout.write(
                f'Total users in database: {User.objects.count()}'
            )
            
            # Helpful next steps
            self.stdout.write('\n' + '='*50)
            self.stdout.write('Next steps:')
            self.stdout.write('1. Start the server: python manage.py runserver')
            self.stdout.write('2. Visit: http://127.0.0.1:8000/api/users/')
            self.stdout.write('3. Try the Django admin: http://127.0.0.1:8000/admin/')
            self.stdout.write('   (Create superuser first: python manage.py createsuperuser)')
            self.stdout.write('='*50)
        else:
            self.stdout.write(
                self.style.WARNING('No new users were created')
            )


# How to use this command:
#
# Basic usage:
#   python manage.py create_sample_users
#
# Create specific number of users:
#   python manage.py create_sample_users --count 10
#
# Clear existing users and create new ones:
#   python manage.py create_sample_users --clear --count 3
#
# Get help:
#   python manage.py help create_sample_users

# Why management commands are useful:
# 1. Automate repetitive tasks
# 2. Set up development environments quickly
# 3. Create data migration scripts
# 4. Perform maintenance operations
# 5. Integrate with deployment scripts