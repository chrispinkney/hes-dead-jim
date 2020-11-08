from setuptools import setup

setup(
    name="He's Dead, Jim",
    version="0.1.05",
    author="Chris Pinkney",
    author_email="hey@chrispinkney.com",
    install_requires=[
        "argparse",
        "requests",
        "beautifulsoup4",
        "datetime ",
        "colorama ",
        "black",
        "pre-commit",
    ],
    entry_points={"console_scripts": ["He-s-Dead-Jim = sample.hdj : main"]},
)
