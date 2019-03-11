import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as version_file:
    version = version_file.read().strip()

setuptools.setup(
    name="pyaim",
    version=version,
    author="Joe Garcia",
    author_email="joe.garcia@cyberark.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/infamousjoeg/pyaim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)