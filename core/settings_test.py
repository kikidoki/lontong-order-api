# Test settings
TEST_RUNNER = 'orders.tests.test_runner.NoDbTestRunner'

# Test-specific settings
if 'test' in sys.argv:
    # Use in-memory SQLite for tests
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    
    # Disable migrations during tests
    class DisableMigrations:
        def __contains__(self, item):
            return True
        
        def __getitem__(self, item):
            return None
    
    MIGRATION_MODULES = DisableMigrations()
    
    # Speed up password hashing
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]
    
    # Disable logging during tests
    import logging
    logging.disable(logging.CRITICAL)