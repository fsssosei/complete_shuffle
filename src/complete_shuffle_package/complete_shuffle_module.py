'''
complete_shuffle - This package is used to complete shuffle the list. 这个包用于对列表完全洗牌。
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

from typing import Final, Callable, Union, Tuple, Optional
from collections.abc import Sized
from collections import namedtuple
from math import pi, e, ceil, log2
from functools import partial
from pure_nrng_package import *
from pure_prng_package import pure_prng

__all__ = ['prng_type_tuple', 'default_prng_type', 'tr_complete_shuffle', 'pr_complete_shuffle', 'tr_complete_cyclic_permutation', 'pr_complete_cyclic_permutation', 'tr_complete_derangement', 'pr_complete_derangement']

True_Randbits = Callable[[int], int]
Unbias = bool

prng_type_tuple: Final[tuple] = tuple(pure_prng.prng_type_list)
default_prng_type = pure_prng.default_prng_type

def _shuffle(x: list, randint: Callable[[int, int], int]) -> None:
    '''
        Shuffle list x in place, and return None.
        
        The formal parameter randint requires a callable object such as rand_int(b, a) that generates a random integer within the specified closed interval.
    '''
    for i in range(len(x) - 1, 0, -1):
        random_location = randint(i, 0)
        x[i], x[random_location] = x[random_location], x[i]


def _random_cyclic_permutation(x: list, randint: Callable[[int, int], int]) -> None:
    '''
        Random cyclic permutation list x in place, and return None.
        
        The formal parameter randint requires a callable object such as rand_int(b, a) that generates a random integer within the specified closed interval.
    '''
    for i in range(len(x) - 1, 0, -1):
        random_location = randint(i - 1, 0)
        x[i], x[random_location] = x[random_location], x[i]


def _random_derangement(x: list, randint: Callable[[int, int], int]) -> None:
    '''
        Random derangement list x in place, and return None.
        An element can never be in the same original position after the shuffle. provides uniform distribution over permutations.
         
        The formal parameter randint requires a callable object such as rand_int(b, a) that generates a random integer within the specified closed interval.
    '''
    sequence_type = namedtuple('sequence_type', ('sequence_number', 'elem'))
    
    x_length = len(x)
    if x_length > 1:
        for i in range(x_length):
            x[i] = sequence_type(sequence_number = i, elem = x[i])
        
        end_label = x_length - 1
        while True:
            for i in range(end_label, 0, -1):
                random_location = randint(i, 0)
                if x[random_location].sequence_number != i:
                    x[i], x[random_location] = x[random_location], x[i]
                else:
                    break
            else:
                if x[0].sequence_number != 0: break
        
        for i in range(x_length):
            x[i] = x[i].elem


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
    if period < 2: raise ValueError('period must be >= 2')
    
    if item_number >= 1:
        if item_number in (1, 2):
            bit_length_of_permutation_number = {1: 1, 2: 2}[item_number]
        else:
            bit_length_of_permutation_number = ceil(log2(2 * pi * item_number) / 2 + log2(item_number / e) * item_number)
        shuffle_number = ceil(bit_length_of_permutation_number / (period.bit_length() - 1))
    else:
        shuffle_number = 0
    return shuffle_number


def tr_complete_shuffle(x: list, *true_randbits_args: Union[True_Randbits, Tuple[True_Randbits, Unbias]]) -> None:
    '''
        Complete shuffle the list based on true random Numbers.
        
        Parameters
        ----------
        x: list
            The list of shuffles.
        
        *true_randbits_args: True_Randbits, or tuple(True_Randbits, Unbias)
            True_Randbits = Callable[[int], int]
            True_Randbits are some callable external true random source objects. Like: secrets.randbits(bit_size)  True_Randbits是一些可调用的外部真随机源对象。形如：secrets.randbits(bit_size)
            If it does not exist, the default is to call the true random source provided by the operating system. 如果不存在的话，则默认调用操作系统提供的真随机源。
            
            Unbias = bool
            Set Unbias to true and enable unbiased processing of true random Numbers used.  Unbias设为真，则对用到的真随机数启用无偏处理。
        
        Returns
        -------
        tr_complete_shuffle: None
            Instead of returning a value, this function directly modifies the content of the argument x.
    '''
    assert isinstance(x, list), f'x must be an list, got type {type(x).__name__}'
    for item in true_randbits_args:
        if isinstance(item, Sized):
            assert isinstance(item, tuple), f'true_randbits_args must be an Callable or tuple, got type {type(item).__name__}'
            assert len(item) == 2, 'There can only be two entries in a tuple, got {len(item)}'
            true_randbits = item[0]; unbias = item[1]
            assert isinstance(true_randbits, Callable), f'True_Randbits must be an Callable, got type {type(true_randbits).__name__}'
            assert isinstance(unbias, bool), f'Unbias must be an bool, got type {type(unbias).__name__}'
        else:
            assert isinstance(item, Callable), f'True_Randbits must be an Callable, got type {type(item).__name__}'
    
    nrng_instance = pure_nrng(*true_randbits_args)
    randint = partial(nrng_instance.true_rand_int)
    _shuffle(x, randint)


def _dynamic_docstring_of_pr_complete_shuffle():
    pr_complete_shuffle.__doc__ = pr_complete_shuffle.__doc__.replace('{default_prng_type}', default_prng_type)
    pr_complete_shuffle.__doc__ = pr_complete_shuffle.__doc__.replace('{prng_type_tuple}', ', '.join([item for item in prng_type_tuple]))


def pr_complete_shuffle(x: list, seed: Optional[int] = None, prng_type: str = default_prng_type) -> None:
    '''
        Complete shuffle the list based on pseudo-random Numbers.
        
        Parameters
        ----------
        x: list
            The list of shuffles.
        
        seed: int, default None
            The seed of a non-negative integer value pseudo-random number generator.
            The default of None is to seed a random number generated by a system.
        
        prng_type: str, default {default_prng_type}
            Specifies the pseudo-random number generator algorithm to use. 指定所用的伪随机数生成器算法。
            Available algorithms: {prng_type_tuple}
        
        Returns
        -------
        pr_complete_shuffle: None
            Instead of returning a value, this function directly modifies the content of the argument x.
        
        Examples
        --------
        >>> seed = 170141183460469231731687303715884105727
        >>> sequence_list = list(range(12))
        >>> pr_complete_shuffle(sequence_list, seed)
        >>> sequence_list
        [3, 6, 2, 10, 11, 0, 7, 9, 1, 4, 8, 5]
    '''
    assert isinstance(x, list), f'x must be an list, got type {type(x).__name__}'
    assert isinstance(seed, (int, type(None))), f'seed must be an int or None, got type {type(seed).__name__}'
    assert isinstance(prng_type, str), f'prng_type must be an str, got type {type(prng_type).__name__}'
    if isinstance(seed, int) and (seed < 0): raise ValueError('seed must be >= 0')
    if prng_type not in prng_type_tuple: raise ValueError('The string for prng_type is not in the list of implemented algorithms.')
    
    prng_period = pure_prng.hash_algorithms_dict[default_prng_type].period
    shuffle_number = _calculate_number_of_shuffles_required(len(x), prng_period)
    
    current_period = prng_period
    prng_instance = pure_prng(seed, prng_type)
    rng_util_prev_prime = rng_util.prev_prime
    prng_instance_rand_int = prng_instance.rand_int
    for _ in range(shuffle_number):
        current_period = int(rng_util_prev_prime(current_period))
        _shuffle(x, prng_instance_rand_int)
_dynamic_docstring_of_pr_complete_shuffle()


def tr_complete_cyclic_permutation(x: list, *true_randbits_args: Union[True_Randbits, Tuple[True_Randbits, Unbias]]) -> None:
    '''
        Complete cyclic permutation the list based on true random Numbers.
        
        Parameters
        ----------
        x: list
            The list of random cyclic permutation.
        
        *true_randbits_args: True_Randbits, or tuple(True_Randbits, Unbias)
            True_Randbits = Callable[[int], int]
            True_Randbits are some callable external true random source objects. Like: secrets.randbits(bit_size)  True_Randbits是一些可调用的外部真随机源对象。形如：secrets.randbits(bit_size)
            If it does not exist, the default is to call the true random source provided by the operating system. 如果不存在的话，则默认调用操作系统提供的真随机源。
            
            Unbias = bool
            Set Unbias to true and enable unbiased processing of true random Numbers used.  Unbias设为真，则对用到的真随机数启用无偏处理。
        
        Returns
        -------
        tr_complete_cyclic_permutation: None
            Instead of returning a value, this function directly modifies the content of the argument x.
    '''
    assert isinstance(x, list), f'x must be an list, got type {type(x).__name__}'
    for item in true_randbits_args:
        if isinstance(item, Sized):
            assert isinstance(item, tuple), f'true_randbits_args must be an Callable or tuple, got type {type(item).__name__}'
            assert len(item) == 2, 'There can only be two entries in a tuple, got {len(item)}'
            true_randbits = item[0]; unbias = item[1]
            assert isinstance(true_randbits, Callable), f'True_Randbits must be an Callable, got type {type(true_randbits).__name__}'
            assert isinstance(unbias, bool), f'Unbias must be an bool, got type {type(unbias).__name__}'
        else:
            assert isinstance(item, Callable), f'True_Randbits must be an Callable, got type {type(item).__name__}'
    
    nrng_instance = pure_nrng(*true_randbits_args)
    randint = partial(nrng_instance.true_rand_int)
    _random_cyclic_permutation(x, randint)


def _dynamic_docstring_of_pr_complete_cyclic_permutation():
    pr_complete_cyclic_permutation.__doc__ = pr_complete_cyclic_permutation.__doc__.replace('{default_prng_type}', default_prng_type)
    pr_complete_cyclic_permutation.__doc__ = pr_complete_cyclic_permutation.__doc__.replace('{prng_type_tuple}', ', '.join([item for item in prng_type_tuple]))


def pr_complete_cyclic_permutation(x: list, seed: Optional[int] = None, prng_type: str = default_prng_type) -> None:
    '''
        Complete cyclic permutation the list based on pseudo-random Numbers.
        
        Parameters
        ----------
        x: list
            The list of random cyclic permutation.
        
        seed: int, default None
            The seed of a non-negative integer value pseudo-random number generator.
            The default of None is to seed a random number generated by a system.
        
        prng_type: str, default {default_prng_type}
            Specifies the pseudo-random number generator algorithm to use. 指定所用的伪随机数生成器算法。
            Available algorithms: {prng_type_tuple}
        
        Returns
        -------
        pr_complete_cyclic_permutation: None
            Instead of returning a value, this function directly modifies the content of the argument x.
        
        Examples
        --------
        >>> seed = 170141183460469231731687303715884105727
        >>> sequence_list = list(range(12))
        >>> pr_complete_cyclic_permutation(sequence_list, seed)
        >>> sequence_list
        [2, 3, 7, 11, 6, 9, 0, 10, 1, 4, 8, 5]
    '''
    assert isinstance(x, list), f'x must be an list, got type {type(x).__name__}'
    assert isinstance(seed, (int, type(None))), f'seed must be an int or None, got type {type(seed).__name__}'
    assert isinstance(prng_type, str), f'prng_type must be an str, got type {type(prng_type).__name__}'
    if isinstance(seed, int) and (seed < 0): raise ValueError('seed must be >= 0')
    if prng_type not in prng_type_tuple: raise ValueError('The string for prng_type is not in the list of implemented algorithms.')
    
    prng_period = pure_prng.hash_algorithms_dict[default_prng_type].period
    shuffle_number = _calculate_number_of_shuffles_required(len(x) - 1, prng_period)
    
    current_period = prng_period
    prng_instance = pure_prng(seed, prng_type)
    rng_util_prev_prime = rng_util.prev_prime
    prng_instance_rand_int = prng_instance.rand_int
    for _ in range(shuffle_number):
        current_period = int(rng_util_prev_prime(current_period))
        _random_cyclic_permutation(x, prng_instance_rand_int)
_dynamic_docstring_of_pr_complete_cyclic_permutation()


def tr_complete_derangement(x: list, *true_randbits_args: Union[True_Randbits, Tuple[True_Randbits, Unbias]]) -> None:
    '''
        Complete derangement the list based on true random Numbers.
        
        Parameters
        ----------
        x: list
            The list of random derangement.
        
        *true_randbits_args: True_Randbits, or tuple(True_Randbits, Unbias)
            True_Randbits = Callable[[int], int]
            True_Randbits are some callable external true random source objects. Like: secrets.randbits(bit_size)  True_Randbits是一些可调用的外部真随机源对象。形如：secrets.randbits(bit_size)
            If it does not exist, the default is to call the true random source provided by the operating system. 如果不存在的话，则默认调用操作系统提供的真随机源。
            
            Unbias = bool
            Set Unbias to true and enable unbiased processing of true random Numbers used.  Unbias设为真，则对用到的真随机数启用无偏处理。
        
        Returns
        -------
        tr_complete_derangement: None
            Instead of returning a value, this function directly modifies the content of the argument x.
        
        Note
        ----
        Can be used for lists with duplicate elements.
    '''
    assert isinstance(x, list), f'x must be an list, got type {type(x).__name__}'
    for item in true_randbits_args:
        if isinstance(item, Sized):
            assert isinstance(item, tuple), f'true_randbits_args must be an Callable or tuple, got type {type(item).__name__}'
            assert len(item) == 2, 'There can only be two entries in a tuple, got {len(item)}'
            true_randbits = item[0]; unbias = item[1]
            assert isinstance(true_randbits, Callable), f'True_Randbits must be an Callable, got type {type(true_randbits).__name__}'
            assert isinstance(unbias, bool), f'Unbias must be an bool, got type {type(unbias).__name__}'
        else:
            assert isinstance(item, Callable), f'True_Randbits must be an Callable, got type {type(item).__name__}'
    
    nrng_instance = pure_nrng(*true_randbits_args)
    randint = partial(nrng_instance.true_rand_int)
    _random_derangement(x, randint)


def _dynamic_docstring_of_pr_complete_derangement():
    pr_complete_derangement.__doc__ = pr_complete_derangement.__doc__.replace('{default_prng_type}', default_prng_type)
    pr_complete_derangement.__doc__ = pr_complete_derangement.__doc__.replace('{prng_type_tuple}', ', '.join([item for item in prng_type_tuple]))


def pr_complete_derangement(x: list, seed: Optional[int] = None, prng_type: str = default_prng_type) -> None:
    '''
        Complete derangement the list based on pseudo-random Numbers.
        
        Parameters
        ----------
        x: list
            The list of random derangement.
        
        seed: int, default None
            The seed of a non-negative integer value pseudo-random number generator.
            The default of None is to seed a random number generated by a system.
        
        prng_type: str, default {default_prng_type}
            Specifies the pseudo-random number generator algorithm to use. 指定所用的伪随机数生成器算法。
            Available algorithms: {prng_type_tuple}
        
        Returns
        -------
        pr_complete_derangement: None
            Instead of returning a value, this function directly modifies the content of the argument x.
        
        Note
        ----
        Can be used for lists with duplicate elements.
        
        Examples
        --------
        >>> seed = 170141183460469231731687303715884105727
        >>> sequence_list = list(range(12))
        >>> pr_complete_derangement(sequence_list, seed)
        >>> sequence_list
        [3, 2, 8, 11, 10, 0, 1, 4, 6, 5, 7, 9]
    '''
    assert isinstance(x, list), f'x must be an list, got type {type(x).__name__}'
    assert isinstance(seed, (int, type(None))), f'seed must be an int or None, got type {type(seed).__name__}'
    assert isinstance(prng_type, str), f'prng_type must be an str, got type {type(prng_type).__name__}'
    if isinstance(seed, int) and (seed < 0): raise ValueError('seed must be >= 0')
    if prng_type not in prng_type_tuple: raise ValueError('The string for prng_type is not in the list of implemented algorithms.')
    
    prng_period = pure_prng.hash_algorithms_dict[default_prng_type].period
    shuffle_number = _calculate_number_of_shuffles_required(len(x), prng_period)
    
    current_period = prng_period
    prng_instance = pure_prng(seed, prng_type)
    rng_util_prev_prime = rng_util.prev_prime
    prng_instance_rand_int = prng_instance.rand_int
    for _ in range(shuffle_number):
        current_period = int(rng_util_prev_prime(current_period))
        _random_derangement(x, prng_instance_rand_int)
_dynamic_docstring_of_pr_complete_derangement()
