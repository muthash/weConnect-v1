import os
import unittest

import coverage
import click
from app import create_app


app = create_app(config_name=os.getenv('APP_SETTINGS'))


COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        'app/tests/*',
        'instance/*',
        '**/__init__.py',
        '**/__pycache__'
    ]
)
COV.start()


@app.cli.command()
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    test()
