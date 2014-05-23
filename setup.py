from distutils.core import setup
from setuptools import find_packages

setup(
    name='pandaslite',
    version='0.1.0',
    author="Greg Lamp",
    author_email="greg@yhathq.com",
    url="https://github.com/yhat/pandaslite",
    packages=find_packages(),
    package_dir={"pandaslite": "pandaslite"},
    package_data={"pandaslite": ["data/*.csv"]},
    description="Like pandas but witout the scary dependencies",
    license='BSD',
    long_description=open('README.rst').read(),
    install_requires=[]
)
