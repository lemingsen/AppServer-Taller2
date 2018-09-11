"""Setup."""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AppServer-Taller2",
    version="0.0.1",
    author="Lucas Hemmingsen",
    author_email="lhemmingsen@fi.uba.ar",
    description="App Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucashemmingsen/AppServer-Taller2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6.4",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
