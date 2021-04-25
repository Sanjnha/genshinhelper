from pathlib import Path

from setuptools import find_packages, setup

long_description = Path('README.en-US.md').read_text(encoding='utf-8')


def load_requirements(filename):
    with Path(filename).open() as f:
        return [line.strip() for line in f if not line.startswith('#')]


__version__ = None
with open('genshinhelper/_version.py', encoding='utf-8') as f:
    exec(f.read())

if not __version__:
    print('Could not find __version__ from genshinhelper/_version.py')
    exit(-1)

setup(
    name='genshinhelper',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/agbulletz/genshinhelper',
    license='GPLv3',
    author='yindan',
    author_email='y1nd4n@outlook.com',
    description='Automatically get Genshin Impact daily check-in rewards from miHoYo bbs and HoYoLAB Community.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='原神 签到 mihoyo hoyolab genshin genshin-impact check-in weibo',
    include_package_data=True,
    install_requires=load_requirements('requirements.txt'),
    tests_require=['pytest'],
    classifiers=[
        # As from https://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.3',
        # 'Programming Language :: Python :: 2.4',
        # 'Programming Language :: Python :: 2.5',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.0',
        # 'Programming Language :: Python :: 3.1',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
    ],
    entry_points={
        'console_scripts': [
            'genshinhelper=genshinhelper.__main__:main'
        ]
    },
    python_requires='>=3.6',
)
