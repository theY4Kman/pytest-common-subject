def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'precondition: mark a fixture to be evaluated before common_subject is invoked',
    )
