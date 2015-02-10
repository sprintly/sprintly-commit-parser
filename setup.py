from setuptools import setup, find_packages


setup(
    name='sprintly_commit_parser',
    version='0.1.0',
    description='Utility for parsing commits for Sprintly commands.',
    long_description='',
    keywords='sprintly, commit, parser',
    author='Nicholas Serra',
    author_email='nserra@quickleft.com',
    url='https://github.com/sprintly/sprintly-commit-parser',
    license='BSD',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
    ]
)
