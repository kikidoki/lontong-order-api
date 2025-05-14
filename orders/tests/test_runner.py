from django.test.runner import DiscoverRunner

class NoDbTestRunner(DiscoverRunner):
    """
    A test runner that doesn't create a test database if there are no database tests.
    """
    def setup_databases(self, **kwargs):
        """
        Override the database creation
        """
        from django.db.backends.base.creation import BaseDatabaseCreation
        
        # Original method
        old_create_test_db = BaseDatabaseCreation.create_test_db
        
        # Override create_test_db to do nothing
        BaseDatabaseCreation.create_test_db = lambda *args, **kwargs: None
        
        # Call the original method with our overridden version
        result = super().setup_databases(**kwargs)
        
        # Restore the original method
        BaseDatabaseCreation.create_test_db = old_create_test_db
        
        return result
    
    def teardown_databases(self, old_config, **kwargs):
        """
        Override the database teardown
        """
        pass