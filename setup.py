#!/usr/bin/env python
import os

from pip.req import parse_requirements
from setuptools import setup, find_packages

setup(
    author="INSS",
    author_email="cpaterso@thoughtworks.com",
    name="rps",
    packages=find_packages("rps"),
    package_dir = {'':'rps'},
    scripts=[
        "rps/chomp_app",
        "rps/ensure_clean_tables",
        "rps/insolvency_practitioner_app",
        "rps/load_user_testing_data",
        "rps/redundancy_payments_service",
    ],
    version=os.environ.get("BUILD_NUMBER", "dev"),
    install_requires=[str(req.req) for req in
                      parse_requirements("rps/requirements.dev.txt")],
    include_package_data=True,
    )
