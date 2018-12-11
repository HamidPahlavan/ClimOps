from setuptools import setup

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
    packages=['climops', 'prepare_data', 'calculate_statistics'],
    keywords='Yale Climate opinion maps, Census',
    #package_data=['data/*'],
    )
