'''
complete_shuffle - This package is used to complete shuffle the list.
Copyright (C) 2020-2021  sosei

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from setuptools import setup, find_packages

with open("README.md", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='complete_shuffle',
    version='1.1.2',
    description='Complete shuffling of lists with true random or pseudo random sequences.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fsssosei/complete_shuffle',
    license='GNU Affero General Public License v3',
    author='sosei',
    author_email='fss.sosei@gmail.com',
    keywords=['complete', 'shuffle', 'cyclic permutation', 'derangement', 'random'],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3.8',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    install_requires=['gmpy2>=2.0.8', 'pure-nrng>=1.1.0', 'pure-prng>=2.9.0']
)
