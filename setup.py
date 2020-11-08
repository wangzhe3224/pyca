import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycax",
    version="1.0.0",
    author="Zhe Wang",
    author_email="wangzhetju@gmail.com",
    description="Cellular Automata, CA, in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wangzhe3224/pyca",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)