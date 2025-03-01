from setuptools import setup, find_packages
import setuptools_scm

setup(
    name="fezrs",
    use_scm_version=True,  # Automatically use version from `VERSION` file or SCM
    setup_requires=["setuptools", "setuptools_scm"],
    packages=find_packages(),  # Automatically find and include packages
    install_requires=[
        "numpy",
        "matplotlib",
        "scikit-image",
        "scikit-learn",
        "fastapi",
        "opencv-python",  # Ensuring compatibility with OpenCV's PyPI package
    ],
    include_package_data=True,  # Include non-code files from MANIFEST.in
    author="Your Name",
    author_email="your.email@example.com",
    description="A brief description of the Fezrs package",
    long_description=open("README.md").read(),  # Read from README.md for PyPI
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fezrs",  # Replace with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust if necessary
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "fezrs=fezrs.__main__:main",  # Replace with actual entry point
        ],
    },
)
