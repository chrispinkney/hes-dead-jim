import setuptools

with open("docs/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="He's Dead, Jim",
    version="1.0.0",
    author="Chris Pinkney",
    author_email="hey@chrispinkney.com",
    description="A command-line tool for finding and reporting dead/broken links in a file or webpage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrispinkney/He-s-Dead-Jim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
