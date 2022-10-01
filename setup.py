from setuptools import setup, find_packages
import versioneer

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="redbox",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Mikael Koli",
    author_email="koli.mikael@gmail.com",
    url="https://github.com/Miksus/red-box.git",
    package_data={package: ["py.typed", "*.pyi", "**/*.pyi"] for package in find_packages()},
    packages=find_packages(),
    zip_safe=False,
    description="Email box reading library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Communications :: Email",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",

        "Intended Audience :: Developers",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Financial and Insurance Industry",
    ],
    include_package_data=True, # for MANIFEST.in
    python_requires='>=3.6.0',

    install_requires = [
        "pydantic"
    ],
)
