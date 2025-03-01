import os

def read_version():
    with open("VERSION") as version_file:
        return version_file.read().strip()

setup(
    name="fezrs",
    version=read_version(),  # Dynamically set version from VERSION file
    packages=["fezrs"],
    install_requires=[
        "numpy",
        "matplotlib",
        "scikit-image",
        "scikit-learn",
        "fastapi",
        "opencv",
    ],
    # Other setup.py fields...
)
