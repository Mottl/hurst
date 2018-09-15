import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    INSTALL_REQUIRES = [l.split('#')[0].strip() for l in fh if not l.strip().startswith('#')]

setuptools.setup(
    name="hurst",
    version="0.0.3",
    author="Dmitry Mottl",
    author_email="dmitry.mottl@gmail.com",
    license="MIT",
    description="Hurst exponent evaluation and R/S-analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mottl/hurst",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    install_requires=INSTALL_REQUIRES,
)
