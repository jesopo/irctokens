import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("VERSION", "r") as version_file:
    version = version_file.read().strip()

setuptools.setup(
    name="irctokens",
    version=version,
    author="jesopo",
    author_email="pip@jesopo.uk",
    description="RFC1459 and IRCv3 protocol tokeniser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jesopo/irctokens",
    packages=setuptools.find_packages(),
    package_data={"irctokens": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Communications :: Chat :: Internet Relay Chat"
    ],
    python_requires='>=3.6'
)
