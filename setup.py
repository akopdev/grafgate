from setuptools import setup, find_packages
from os import path

dir = path.abspath(path.dirname(__file__))

setup(
    # Basic info
    name="grafgate",
    version="0.0.1",
    author="Akop Kesheshyan",
    author_email="hello@akop.dev",
    url="https://github.com/akopkesheshyan/grafgate",
    license="MIT",
    description="Toolkit for building Grafana data source backend",
    long_description=open(path.join(dir, "README.md"), encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
    ],
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "pydantic"
    ],
    extras_require={
        "dev": [
            "flake8",
            "safety",
            "pydocstyle",
            "piprot",
            "pytest",
            "pytest-cov",
            "pytest-asyncio",
        ],
    },
    zip_safe=False,
    platforms="any",
)
