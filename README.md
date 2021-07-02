# complete_shuffle

![PyPI](https://img.shields.io/pypi/v/complete_shuffle?color=red)
![PyPI - Status](https://img.shields.io/pypi/status/complete_shuffle)
![GitHub Release Date](https://img.shields.io/github/release-date/fsssosei/complete_shuffle)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/fsssosei/complete_shuffle.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/fsssosei/complete_shuffle/context:python)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bf34f8d12be84b4492a5a3709df0aae5)](https://www.codacy.com/manual/fsssosei/complete_shuffle?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fsssosei/complete_shuffle&amp;utm_campaign=Badge_Grade)
![PyPI - Downloads](https://img.shields.io/pypi/dw/complete_shuffle?label=PyPI%20-%20Downloads)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/complete_shuffle)
![PyPI - License](https://img.shields.io/pypi/l/complete_shuffle)

*Complete shuffling of lists with true random or pseudo random sequences.*

Multiple external true random sources can be accessed to shuffle the list.

In addition to the shuffle function, there are also random cyclic permutation functions, and the derangement function.

## Installation

Installation can be done through pip. You must have python version >= 3.8

	pip install complete-shuffle

## Usage

The statement to import the package:

	from complete_shuffle_package import *
	
Example:

	>>> prng_period = calculate_number_of_shuffles_required(12, 'prng_period')
	>>> seed = 170141183460469231731687303715884105727 & prng_period.bit_length()
	#The entropy of the seed must not be less than the number of permutations in the list.(Calculate with "calculate_number_of_shuffles_required" function)
	
	>>> sequence_list = list(range(12))
	>>> pr_complete_shuffle(sequence_list, seed)
	>>> sequence_list
	[11, 5, 7, 3, 0, 4, 6, 9, 10, 1, 2, 8]
	
	>>> sequence_list = list(range(12))
	>>> pr_complete_cyclic_permutation(sequence_list, seed)
	>>> sequence_list
	[6, 11, 5, 7, 3, 0, 4, 9, 10, 1, 2, 8]
	
	>>> sequence_list = list(range(12))
	>>> pr_complete_derangement(sequence_list, seed)
	>>> sequence_list
	[7, 3, 11, 2, 0, 10, 5, 4, 6, 1, 9, 8]
