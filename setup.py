# coding=utf-8
"""Python Bold Smart Lock setup script."""
from setuptools import setup

_VERSION = "0.2.0"


def readme():
    with open("README.md") as desc:
        return desc.read()


setup(
    name="bold_smart_lock",
    packages=["bold_smart_lock"],
    version=_VERSION,
    description="A Python library to communicate with Bold Smart Lock (https://boldsmartlock.com)",
    author="Westenberg",
    author_email="lauren@westenberg.dev",
    url="https://github.com/westenberg/bold_smart_lock",
    license="MIT",
    include_package_data=True,
    install_requires=[
        "aiohttp",
        "asyncio",
        "aioresponses",
        "pytest",
        "pytest-asyncio"
    ],
    test_suite="tests",
    keywords=[
        "bold",
        "smart lock",
        "home automation",
    ],
    classifiers=[
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Home Automation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
