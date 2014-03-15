from distutils.core import setup

setup(
    name = 'django-sync-google-contacts',
    packages = ['sync_google_contacts'],
    version = '0.1',
    #include_package_data=True,
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        'sync_google_contacts': [
            'templates/*',
            'static/sync_google_contacts/*',
            ],
    },

    description = 'Manage groups and user via jtable',
    author = 'Erwin Sprengers',
    author_email = 'sprengee54@gmail.com',
    url = 'http://pypi.python.org/pypi//django-sync-google-contacts',   # use the URL to the github repo
    keywords = ['django', 'admin', 'google', 'contacts', ], # arbitrary keywords
    classifiers = [],
)
