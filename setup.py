from distutils.core import setup

setup(
    name='pyStatikMan',
    version='0.9',
    packages=['components', 'common', 'apiresources'],
    url='https://zubeax.github.io/',
    license='GNU',
    author='Axel Zuber',
    author_email='zubeax@github.com',
    description='Commit Comments on Blog Posts to Github Pages Repository',
    requires=['flask', 'jira-python', 'pyodbc', 'flask-restful', 'flask-httpauth', 'httplib2']
)
