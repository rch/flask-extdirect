"""
Flask-Sencha
-------------

This is the description for that library
"""
from setuptools import setup


setup(
    name='Flask-Sencha',
    version='0.1',
    url='http://github.com/rch/flask-extdirect',
    license='BSD',
    author='Ryan C. Hill',
    author_email='@zndx.org',
    description='Very short description',
    long_description=__doc__,
    # py_modules=['flask_extdirect'],
    packages=[
        'flask_sencha',
        'flask_sencha.direct',
        'flask_sencha.direct.message',
        'flask_sencha.direct.message.action',
        'flask_sencha.direct.message.action.data',
        'flask_sencha.direct.resource',
        'flask_sencha.direct.resource.provider',
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'python-dateutil',
        'Flask',
        'celery',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)