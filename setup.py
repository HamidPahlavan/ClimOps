from setuptools import setup, find_packages

with open("README", 'r') as f:
    long_description = f.read()

setup(
    name='climops',
    version='0.1.0',
    description='''
                Python interface to get statistical relationships
                from Yale Climate opinion maps and Census
                ''',
    url='https://github.com/https://github.com/HamidPahlavan/climops',
    license='MIT',
    author='''
            Robin Clancy, Rebeca de Buen,
            Hamid Pahlavan and Yakelyn R. Jauregui
            ''',
    author_email='rclancy@uw.edu',
    packages=find_packages(),
    keywords='Yale Climate opinion maps, Census',
    package_data=['data/*'],
    )
