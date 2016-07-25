#!/usr/bin/python

from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()

setup(name='glucoregulatory',
    version='0.0.0', # http://semver.org/
    description='Glucoregulatory model for the openai gym.',
    long_description=readme(),
    author="Nathan West",
    author_email="nateewest@gmail.com",
    maintainer="Ben West",
    url="https://github.com/n-west/aps-gym",
    packages=find_packages( ),
    include_package_data = True,
    install_requires = [
      'gym', 
    ],
    dependency_links = [

    ],
    scripts = [

    ],
    entry_points = {

    },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=False,
)

#####
# EOF
