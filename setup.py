import io
import os
import pathlib
import setuptools

import slican_client

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Automatically captured required modules for install_requires in requirements.txt
with io.open(os.path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]

setuptools.setup(
    name = 'slican_client',
    description = 'The client establishing connection with the server socket of the Slican telephone exchange.',
    version = slican_client.__version__,
    packages = setuptools.find_packages(), # list of all packages
    install_requires = install_requires,
    python_requires = '>=3.6', # any python greater than 3.6
    entry_points='''
            [console_scripts]
            slican_client = slican_client.__main__:main
        ''',
    author = 'Wojciech Sobczak',
    author_email = 'wsobczak@gmail.com',
    long_description = README,
    long_description_content_type = 'text/markdown',
    license = 'MIT',
    # url='https://github.com/CITGuru/cver',
    # download_url='https://github.com/CITGuru/cver/archive/1.0.0.tar.gz',
    dependency_links = dependency_links
)