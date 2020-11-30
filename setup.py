import setuptools

with open("docs/README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="He's Dead, Jim",
    version="1.0.5",
    author="Chris Pinkney",
    author_email="hey@chrispinkney.com",
    description="A command-line tool for finding and reporting dead/broken links in a file or webpage.",
    url="https://github.com/chrispinkney/He-s-Dead-Jim",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "argparse == 1.4.0",
        "requests == 2.24.0",
        "beautifulsoup4 == 4.9.1",
        "datetime == 4.3",
        "colorama == 0.4.4",
        "black == 20.8b1",
        "flake8 == 3.8.4",
        "pre-commit == 2.7.1",
        "pytest == 6.1.2",
        "pytest-cov == 2.10.1",
    ],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "hdj = src.hdj:main_wrapper",
        ]
    },
    python_requires=">=3.6",
)
