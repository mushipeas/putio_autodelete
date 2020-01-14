from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))

packages = ["putio_autodelete"]

about = {}
with open(
    os.path.join(here, "putio_autodelete", "__version__.py"), "r", encoding="utf-8"
) as f:
    exec(f.read(), about)

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().strip().split("\n")

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=packages,
    package_data={"": ["LICENSE"],},
    package_dir={"putio_autodelete": "putio_autodelete"},
    include_package_data=True,
    python_requires="!=2.7, >=3.0.*",
    install_requires=requirements,
    license=about["__license__"],
    keywords="putio automation file-manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        "console_scripts": ["putio_autodelete = putio_autodelete.putio_autodelete:main"]
    },
)
