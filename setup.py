from setuptools import setup, find_packages
from configparser import ConfigParser


def read_version_from_bumpversion():
    config = ConfigParser()
    config.read(".bumpversion.cfg")
    return config["bumpversion"]["current_version"]


setup(
    name="fezrs",
    version=read_version_from_bumpversion(),
    setup_requires=["setuptools", "setuptools_scm"],
    packages=find_packages(include=["fezrs", "fezrs.*"]),
    install_requires=[
        "numpy",
        "pydantic",
        "matplotlib",
        "scikit-learn",
        "scikit-image",
        "opencv-python",
    ],
    author="Mahdi Farmahinifarahani, Hooman Mirzaee, Mahdi Nedaee, Mohammad Hossein Kiani Fayz Abadi, Yoones Kiani Feyz Abadi, Erfan Karimzadehasl, Parsa Elmi",
    author_email="aradfarahani@aol.com",
    description="Feature Extraction and Zoning for Remote Sensing (FEZrs)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FEZtool-team/FEZrs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
