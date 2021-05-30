import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="attack-detectors-comparer",
    version="1.0.0",
    author="Boladji Vinny",
    author_email="vinny.adjibi@outlook.com",
    description="A package to compare cyber-security attack detection"\
            "techniques.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/boladjivinny/attack-detectors-comparer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv2 License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires='>=3.6',
    install_requires = [
        'matplotlib>=3.4.2',
        'numpy>=1.20.2',
        'pandas>=1.2.4',
        'scikit-learn>=0.24.2',
    ]
)