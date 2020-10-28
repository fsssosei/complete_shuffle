# completely_shuffle

![PyPI](https://img.shields.io/pypi/v/completely_shuffle?color=red)
![PyPI - Status](https://img.shields.io/pypi/status/completely_shuffle)
![GitHub Release Date](https://img.shields.io/github/release-date/fsssosei/completely_shuffle)
[![Build Status](https://scrutinizer-ci.com/g/fsssosei/completely_shuffle/badges/build.png?b=main)](https://scrutinizer-ci.com/g/fsssosei/completely_shuffle/build-status/main)
[![Code Intelligence Status](https://scrutinizer-ci.com/g/fsssosei/completely_shuffle/badges/code-intelligence.svg?b=main)](https://scrutinizer-ci.com/code-intelligence)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/fsssosei/completely_shuffle.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/fsssosei/completely_shuffle/context:python)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bf34f8d12be84b4492a5a3709df0aae5)](https://www.codacy.com/manual/fsssosei/completely_shuffle?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fsssosei/completely_shuffle&amp;utm_campaign=Badge_Grade)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/fsssosei/completely_shuffle/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/fsssosei/completely_shuffle/?branch=main)
![PyPI - Downloads](https://img.shields.io/pypi/dw/completely_shuffle?label=PyPI%20-%20Downloads)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/completely_shuffle)
![PyPI - License](https://img.shields.io/pypi/l/completely_shuffle)

*Complete shuffling of lists with true random or pseudo random sequences.*

Multiple external true random sources can be accessed to shuffle the list.

## Installation

Installation can be done through pip. You must have python version >= 3.7

	pip install pure-prng

## Usage

The statement to import the package:

	from completely_shuffle_package import *
	
Example:

	>>> seed = 170141183460469231731687303715884105727
	>>> sequence_list = list(range(12))
	>>> pr_completely_shuffle(sequence_list, seed)
	>>> sequence_list
	[3, 6, 2, 10, 11, 0, 7, 9, 1, 4, 8, 5]
