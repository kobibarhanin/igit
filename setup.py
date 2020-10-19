import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

package_conf = {}

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "igit", "__version__.py")) as f:
    exec(f.read(), package_conf)

setuptools.setup(
    name="igit",
    version=package_conf['__version__'],
    author="kobibarhanin",
    author_email="",
    description="Interactive git and more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kobibarhanin/igit",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "igit=igit:cli",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["attrs==19.3.0", "blessed==1.17.6", "fire==0.3.1", "gitdb==4.0.5", "GitPython==3.1.7", "importlib-metadata==1.7.0", "inquirer==2.7.0", "more-itertools==8.4.0", "packaging==20.4", "pluggy==0.13.1", "py==1.9.0", "pyparsing==2.4.7", "pytest==5.4.3", "python-editor==1.0.4", "PyYAML==5.3.1", "readchar==2.0.1", "six==1.15.0", "smmap==3.0.4", "termcolor==1.1.0", "wcwidth==0.2.5", "zipp==3.1.0", "emoji==0.5.4", "PyInquirer==1.0.3"],
    python_requires='>=3.7',
)
