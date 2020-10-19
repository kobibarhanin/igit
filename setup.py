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
            "igit=igit.cli:run",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # TODO - remove unnecessary dependencies
    install_requires=["astroid==2.4.2" ,"attrs==20.2.0" ,"blessed==1.17.6" ,"click==7.1.2" ,"emoji==0.6.0" ,"fire==0.3.1" ,"gitdb==4.0.5" ,"gitignore-parser==0.0.8" ,"GitPython==3.1.9" ,"importlib-metadata==2.0.0" ,"iniconfig==1.0.1" ,"inquirer==2.7.0" ,"invoke==1.4.1" ,"isort==5.5.4" ,"lazy-object-proxy==1.4.3" ,"mccabe==0.6.1" ,"more-itertools==8.5.0" ,"packaging==20.4" ,"pathlib2==2.3.5" ,"pluggy==0.13.1" ,"prompt-toolkit==1.0.14" ,"psutil==5.7.2" ,"py==1.9.0" ,"Pygments==2.7.1" ,"PyInquirer==1.0.3" ,"pylint==2.6.0" ,"pyparsing==2.4.7" ,"pytest==6.1.0" ,"python-dotenv==0.14.0" ,"python-editor==1.0.4" ,"PyYAML==5.3.1" ,"readchar==2.0.1" ,"regex==2020.9.27" ,"six==1.15.0" ,"smmap==3.0.4" ,"termcolor==1.1.0" ,"toml==0.10.1" ,"typed-ast==1.4.1" ,"wcwidth==0.2.5" ,"wrapt==1.12.1" ,"zipp==3.2.0"],
    python_requires='>=3.7',
)
