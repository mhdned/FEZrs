from setuptools import setup, find_packages

setup(
    name="fezrs",
    version="0.3.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "scikit-image",
        "scikit-learn",
        "fastapi",
        "opencv-python"
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
    python_requires=">=3.8",
)
