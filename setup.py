'''
setup.py is used to build an application (say ML) as a package
'''

# find_packages identifies all the packages used in the application
from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path:str)->List[str]:
    '''
    this function returns the list of requirements
    '''
    requirements = []
    with open(file_path) as file_object:
        requirements = file_object.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if "-e ." in requirements:
            requirements.remove("-e .")
    
    return requirements


#metadata of the application
setup(
    name='MLOps',
    version='0.0.1',
    author='Anirudh Nuti',
    author_email='nuti.krish4@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)