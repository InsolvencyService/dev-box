#!/usr/bin/env python
import os

from pip.req import parse_requirements
from setuptools import setup, find_packages

setup(
    author="INSS",
    author_email="cpaterso@thoughtworks.com",
    name="redundancy_payments_alpha",
    packages=find_packages("redundancy_payments_alpha"),
    package_dir = {'':'redundancy_payments_alpha'},
    scripts=[
        "redundancy_payments_alpha/redundancy_payments_service",
        "redundancy_payments_alpha/ensure_clean_tables"
    ],
    version=os.environ.get("BUILD_NUMBER", "dev"),
    install_requires=[str(req.req) for req in
                      parse_requirements("redundancy_payments_alpha/requirements.dev.txt")],
    include_package_data=True,
    )
