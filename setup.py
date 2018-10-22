import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SonosQ",
    version="0.0.1",
    author="maziara",
    author_email="maziara2@gmail.com",
    description="A package to export Sonos Queue as M3U",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maziara/SonosQ.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)