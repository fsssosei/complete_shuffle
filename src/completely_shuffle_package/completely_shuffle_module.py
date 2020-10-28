'''
completely_shuffle - This package is used to completely shuffle the list. 这个包用于对列表完全洗牌。
Copyright (C) 2020  sosei
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

from typing import Final, Callable, Optional
from pure_nrng_package import *
from pure_prng_package import pure_prng

__all__ = ['prng_algorithms_tuple', 'default_prng_type', 'tr_completely_shuffle', 'pr_completely_shuffle']

prng_algorithms_tuple: Final[tuple] = tuple(pure_prng.prng_algorithms_list)
default_prng_type = 'xoshiro256++'

def _shuffle(x: list, randint: Callable[[int, int], int]) -> None:
    '''
        Shuffle list x in place, and return None.
        
        The formal parameter randint requires a callable object such as rand_int(b, a) that generates a random integer within the specified closed interval.
    '''
    for i in range(len(x) - 1, 0, -1):
        random_location = randint(i, 0)
        x[i], x[random_location] = x[random_location], x[i]


def _calculate_number_of_shuffles_required(item_number: int, period: int) -> int:
    '''
        The number of permutations of a list item is the factorial of the number of list items. The number of binary digits of the total number of permutations can be calculated by Stirling's formula.
        When the number of pseudo-random number period used for shuffling is less than the number of permutations in the list, multiple shuffling is required.
        A shuffle is sufficient if the number of pseudo-random period multiplied by each shuffle is greater than the number of permutations in the list.
        
        Parameters
        ----------
        item_number: int
            The number of items to shuffle the list.要洗牌列表的项数。
        
        period: int
            Eigenperiod of a random number generator (maximum period) 随机数生成器的本征周期（最大周期）
            period must be >= 2
    '''
    import math
    
    if item_number > 0:
        bit_length_of_permutation_number = math.ceil(math.log2(2 * math.pi * item_number) / 2 + math.log2(item_number / math.e) * item_number)
        shuffle_number = math.ceil(bit_length_of_permutation_number / (period.bit_length() - 1))
    else:
        shuffle_number = 0
    return shuffle_number


def tr_completely_shuffle(x: list, *true_randbits_tuple: Callable[[int], int], unbias: bool = True) -> None:
    '''
        Completely shuffle the list based on true random Numbers.
        
        Parameters
        ----------
        x: list
            The list of shuffles.
        
        *true_randbits_tuple: Callable
            Some callable external true random source objects. Like: secrets.randbits(bit_size) 一些可调用的外部真随机源对象。形如：secrets.randbits(bit_size)
        
        unbias: bool, default True
            Set to true, and enable unbiased processing for the true random Numbers used. 设为真，则对用到的真随机数启用无偏处理。
        
        Returns
        -------
        tr_completely_shuffle: None
            Instead of returning a value, this function directly modifies the content of the argument x.
    '''
    assert isinstance(x, list), f'x must be an list, got type {type(x).__name__}'
    for true_randbits in true_randbits_tuple:
        assert isinstance(true_randbits, Callable), f'true_randbits must be an Callable, got type {type(true_randbits).__name__}'
    
    from functools import partial
    
    nrng_instance = pure_nrng(*true_randbits_tuple)
    randint = partial(nrng_instance.true_rand_int, unbias = unbias)
    _shuffle(x, randint)


def pr_completely_shuffle(x: list, seed: Optional[int] = None, prng_type: str = default_prng_type) -> None:
    '''
        Completely shuffle the list based on pseudo-random Numbers.
        
        Parameters
        ----------
        x: list
            The list of shuffles.
        
        seed: int, default None
            The seed of a non-negative integer value pseudo-random number generator.
            The default of None is to seed a random number generated by a system.
        
        prng_type: str, default default_prng_type
            Specifies the pseudo-random number generator algorithm to use. 指定所用的伪随机数生成器算法。
        
        Returns
        -------
        pr_completely_shuffle: None
            Instead of returning a value, this function directly modifies the content of the argument x.
        
        Examples
        --------
        >>> seed = 170141183460469231731687303715884105727
        >>> sequence_list = list(range(12))
        >>> pr_completely_shuffle(sequence_list, seed)
        >>> sequence_list
        [3, 6, 2, 10, 11, 0, 7, 9, 1, 4, 8, 5]
    '''
    assert isinstance(x, list), f'x must be an list, got type {type(x).__name__}'
    assert isinstance(seed, (int, type(None))), f'seed must be an int or None, got type {type(seed).__name__}'
    if isinstance(seed, int) and (seed < 0): raise ValueError('seed must be >= 0')
    if prng_type not in prng_algorithms_tuple: raise ValueError('The string for prng_type is not in the list of implemented algorithms.')
    
    prng_period = pure_prng.prng_period_dict[default_prng_type]
    shuffle_number = _calculate_number_of_shuffles_required(len(x), prng_period)
    
    current_period = prng_period
    prng_instance = pure_prng(seed, prng_type)
    for _ in range(shuffle_number):
        current_period = int(rng_util.prev_prime(current_period))
        _shuffle(x, prng_instance.rand_int)