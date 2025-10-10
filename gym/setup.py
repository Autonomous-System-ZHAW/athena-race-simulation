from setuptools import setup, find_packages

setup(
    name="f110_gym",
    version="0.2.1",
    author="Hongrui Zheng",
    author_email="billyzheng.bz@gmail.com",
    url="https://f1tenth.org",
    packages=find_packages(),
    install_requires=[
        "gymnasium==0.29.1",
        "numpy>=1.26.0",
        "pillow>=10.0.0",
        "scipy>=1.11.0",
        "numba>=0.59.0",
        "pyyaml>=6.0.0",
        "pygame",
        "pyopengl",
    ],
)
