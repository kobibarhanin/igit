import setuptools
from pathlib import Path
import pkg_resources

package_conf = {}
with open(Path("igit") / "__version__.py") as f:
    exec(f.read(), package_conf)
with open("README.md", "r") as fh:
    package_conf['description'] = fh.read()

with Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setuptools.setup(
    name="igit",
    version=package_conf['__version__'],
    author="kobi",
    author_email="",
    description="Interactive git and more",
    long_description=package_conf['description'],
    long_description_content_type="text/markdown",
    url="https://github.com/kobibarhanin/igit",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "igit=igit.cli:run",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    install_requires=install_requires,
    python_requires='>=3.7',
)
