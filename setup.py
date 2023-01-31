# coding=utf-8
"""Python Bold Smart Lock setup script."""
from pathlib import Path
from setuptools import setup

_VERSION = "0.3.9"

long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name="bold_smart_lock",
    packages=["bold_smart_lock"],
    version=_VERSION,
    description="Python library to communicate with Bold Smart Lock (https://boldsmartlock.com)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Westenberg",
    author_email="lauren@westenberg.dev",
    url="https://github.com/westenberg/bold_smart_lock",
    license="MIT",
    include_package_data=True,
    install_requires=[
        "aiohttp",
        "asyncio",
    ],
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
        "Programming Language :: Python :: 3.9",
        "Topic :: Home Automation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
