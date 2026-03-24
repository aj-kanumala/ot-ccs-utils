from setuptools import setup, find_packages

setup(
    name="ot-ccs-utils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "matplotlib",
        "time",
        "POT",
    ],
    dependency_links=["git+https://github.com/PythonOT/POT.git#egg=POT"],
    python_requires=">=3.8",
)