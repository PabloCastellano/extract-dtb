#!/usr/bin/env python
from setuptools import setup


setup(
    name="extract-dtb",
    packages=["extract_dtb"],
    version="1.2.2",
    entry_points={"console_scripts": ["extract-dtb = extract_dtb.extract_dtb:main"]},
    description="Tool to split a kernel image with appended dtbs into separated kernel and dtb files.",
    long_description=open("README.md").read(),
    author="Pablo Castellano",
    author_email="pablo@anche.no",
    url="https://github.com/PabloCastellano/extract-dtb/",
    download_url="https://github.com/PabloCastellano/extract-dtb/archive/master.zip",
    keywords=["dtb", "android", "kernel"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    license="GPLv3+",
    data_files=[("", ["LICENSE", "CHANGES.md"])],
    include_package_data=True,
    zip_safe=False,
    long_description_content_type="text/markdown",
)
