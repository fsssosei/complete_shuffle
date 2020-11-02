# complete_shuffle

![PyPI](https://img.shields.io/pypi/v/complete_shuffle?color=red)
![PyPI - Status](https://img.shields.io/pypi/status/complete_shuffle)
![GitHub Release Date](https://img.shields.io/github/release-date/fsssosei/complete_shuffle)
[![Build Status](https://scrutinizer-ci.com/g/fsssosei/complete_shuffle/badges/build.png?b=main)](https://scrutinizer-ci.com/g/fsssosei/complete_shuffle/build-status/main)
[![Code Intelligence Status](https://scrutinizer-ci.com/g/fsssosei/complete_shuffle/badges/code-intelligence.svg?b=main)](https://scrutinizer-ci.com/code-intelligence)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/fsssosei/complete_shuffle.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/fsssosei/complete_shuffle/context:python)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bf34f8d12be84b4492a5a3709df0aae5)](https://www.codacy.com/manual/fsssosei/complete_shuffle?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fsssosei/complete_shuffle&amp;utm_campaign=Badge_Grade)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/fsssosei/complete_shuffle/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/fsssosei/complete_shuffle/?branch=main)
![PyPI - Downloads](https://img.shields.io/pypi/dw/complete_shuffle?label=PyPI%20-%20Downloads)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/complete_shuffle)
![PyPI - License](https://img.shields.io/pypi/l/complete_shuffle)

*Complete shuffling of lists with true random or pseudo random sequences.*

Multiple external true random sources can be accessed to shuffle the list.

In addition to the shuffle function, there are also random cyclic permutation functions.

## Installation

Installation can be done through pip. You must have python version >= 3.8

	pip install complete-shuffle

## Usage

The statement to import the package:

	from complete_shuffle_package import *
	
Example:

	>>> seed = 170141183460469231731687303715884105727
	>>> sequence_list = list(range(12))
	>>> pr_complete_shuffle(sequence_list, seed)
	>>> sequence_list
	[3, 6, 2, 10, 11, 0, 7, 9, 1, 4, 8, 5]
	
	>>> sequence_list = list(range(12))
	>>> pr_complete_cyclic_permutation(sequence_list, seed)
	>>> sequence_list
	[2, 3, 7, 11, 6, 9, 0, 10, 1, 4, 8, 5]
