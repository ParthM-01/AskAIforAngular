from setuptools import find_packages, setup
from typing import List


def get_requirements(file_path: str) -> List[str]:
    """Return the list of requirements from a file."""
    requirements: List[str] = []
    with open(file_path) as file_obj:
        requirements = [req.strip() for req in file_obj.readlines()]
        requirements = [req for req in requirements if req and not req.startswith('#')]

        if '-e .' in requirements:
            requirements.remove('-e .')

    return requirements


setup(
    name='AskAIforAngular',
    version='0.0.1',
    author='Parth',
    author_email='parthmangukiya020@gmail.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=get_requirements('requirements.txt')
    # include_package_data=True,
)
