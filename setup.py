# Modules libraries
from setuptools import find_packages, setup

# Requirements
requirements = []
with open('requirements.txt') as f:
    requirements = [line for line in f.read().splitlines() if not line.startswith('#')]

# Long description
long_description = '' # pylint: disable=invalid-name
with open('README.md', 'r') as f:
    long_description = f.read()

# Setup configurations
setup(
    name='githubci-runner',
    use_scm_version=True,
    author='Elbek Khoshimjonov',
    author_email='noreply@gmail.com',
    license='Apache License 2.0',
    description='Launch .github-ci.yml jobs locally',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/elb3k/githubci-runner',
    packages=find_packages(exclude=['tests']),
    setup_requires=['setuptools_scm'],
    install_requires=requirements,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    keywords='github-ci local gcil pipeline',
    python_requires='>=3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
    entry_points={
        'console_scripts': [
            'githubci-runner = githubci_runner.cli:main',
        ],
    },
)
