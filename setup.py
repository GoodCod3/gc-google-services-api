from setuptools import setup, find_packages
from gc_google_services_api import __version__

setup(
      name='gc_google_services_api',
      version=__version__,
      packages=find_packages(),
      author='Jonathan Rodriguez Alejos',
      author_email='jrodriguez.5716@gmail.com',
      install_requires=open('requirements.txt').read().splitlines()
)