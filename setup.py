from setuptools import setup, find_packages

__author__ = 'Kirill Kupriyanov'
__author_email__ = 'kupriyanovkirill@gmail.com'


def version():
    with open('VERSION') as _fd_:
        return _fd_.read()


def requirements():
    with open('requirements.txt', 'r') as _fd_:
        return _fd_.read().split('\n')


def readme():
    with open('README.md') as _fd_:
        return _fd_.read()


ENTRY_POINTS = {
    'console_scripts': [
        'gsl=goodsteel_ledger:main'
    ]
}

setup(
    name='gsl',
    version=version(),
    description='Goodsteel Ledger -- a program for building own distributed ledger',
    long_description=readme(),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Topic :: Security :: Cryptography',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux  ',
    ],
    author=__author__,
    author_email=__author_email__,
    package_dir={
        '': 'src',
    },
    packages=find_packages('src'),
    include_package_data=True,
    install_requires=requirements(),
    zip_safe=False,
    entry_points=ENTRY_POINTS
)

