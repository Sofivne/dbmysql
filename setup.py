from setuptools import setup, find_packages

setup(
    name='dbmysql',
    version='1.0.5',  
    author='Sofivne',
    description='Un package Python pour gérer les interactions avec une base de données MySQL',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Sofivne/dbmysql',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'mysql-connector-python',
        'python-dotenv'
    ],
)
