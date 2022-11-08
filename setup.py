import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyrbaskets',
    version='0.0.1',
    author='H4N9U1',
    author_email='h4n9u1@h4n9u1.com',
    description='Request Baskets RESTful API Wrapper for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls = {
        'Bug Tracker': ''
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operation System :: OS Independent'
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires=">=3.10"
)