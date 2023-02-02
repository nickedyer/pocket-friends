import setuptools
import pocket_friends

with open('requirements.txt') as fh:
    required = fh.read().splitlines()

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='Pocket Friends',
    version=pocket_friends.__version__,
    author='Nicholas Dyer',
    description='A virtual friend for you to take care of and have fun with!',
    license='GNU GPL-3.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nickedyer/pocket-friends',
    packages=setuptools.find_packages(),
    # https://pypi.org/classifiers/
    classifiers=[
    ],
    install_requires=required,
    python_requires='>=3.10',
    include_package_data=True,
)
