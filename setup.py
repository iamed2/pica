"""
To install:

    python3.5 setup.py install

to test:

    python3.5 setup.py nosetests
"""
from setuptools import setup


setup(
    name='pica',
    description='A curses-based probabilistic cellular automata.',
    long_description=open('README.md').read(),
    version='0.1.0',
    author='Brendan Curran-Johnson',
    author_email='brendan@bcjbcj.ca',
    license='MPL 2.0',
    url='https://github.com/bcj/pica',
    packages=('pica',),
    entry_points = {
        'console_scripts': (
            'pica = pica.cli:main',
        )
    },
    tests_require=(
        'pica',
    ),
    classifiers=(
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: Console :: Curses",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Artistic Software",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Interpreters",
    ),
)

