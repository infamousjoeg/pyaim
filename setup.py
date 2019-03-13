import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyaim",
    version="1.0.0",
    author="Joe Garcia",
    author_email="joe.garcia@cyberark.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/infamousjoeg/pyaim",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='cyberark aim aam identity access security pam pim pas',
    project_urls={
        'Bug Reports': 'https://github.com/infamousjoeg/pyaim/issues/new?assignees=&labels=&template=bug_report.md&title=',
        'Feature Requests': 'https://github.com/infamousjoeg/pyaim/issues/new?assignees=&labels=&template=feature_request.md&title=',
        'Source': 'https://github.com/infamousjoeg/pyaim'
    }
)