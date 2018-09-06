import os
from setuptools import setup, find_packages


README = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')


DEPENDENCIES = [
    'django-cms>=2.3.5pbs,<2.3.5pbs.1000',
    'django-cms-layouts>=0.1.1.pbs,<0.1.1.pbs1000',
    'django-select2 >4.3.1,<4.3.2',
    'django-filer>=0.9pbs,<0.9pbs.1000',
    'python-dateutil >= 2.2',
]

DEPENDENCY_LINKS = [
    'https://github.com/pbs/django-cms-layouts/tarball/master#egg=django-cms-layouts-0.1'
]

setup(
    name='django-cms-blogger',
    version='0.7.0.pbs.16',
    description='Django CMS blogging tool that lets users create blogs '
                'using layouts created from CMS pages.',
    long_description=open(README, 'r').read(),
    author='Laura Feier',
    author_email='feierlaura10@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=DEPENDENCIES,
    dependency_links=DEPENDENCY_LINKS,
    setup_requires=["setuptools-tasks"],
    classifiers=[],
)
