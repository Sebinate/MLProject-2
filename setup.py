from setuptools import setup, find_packages
from typing import List

def package_parser(path) -> List[str]:
    try: 
        package_list = []
        with open(path, 'r') as file:
            for package in file.readlines():
                package = package.strip()
                if package and package != "-e .":
                    package_list.append(package)
            
        return package_list
    
    except FileNotFoundError:
        print("Requirements text file not found")
        
setup(name = "Network Security Project",
      author = "Sebastian James Sampao",
      version = '0.0.1',
      author_email = "sebastiansampao@gmail.com",
      packages = find_packages(),
      install_requires = package_parser('requirements.txt'))