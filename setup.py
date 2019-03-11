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
    license="MIT",
    platform="OS Independent",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='cyberark aim aam identity access security pam pim pas',
    python_requires='>=3.*.*, <4',
    project_urls={
        'Bug Reports': 'https://github.com/infamousjoeg/pyaim/issues/new?assignees=&labels=&template=bug_report.md&title=',
        'Feature Requests': 'https://github.com/infamousjoeg/pyaim/issues/new?assignees=&labels=&template=feature_request.md&title=',
        'Source': 'https://github.com/infamousjoeg/pyaim'
    }
)