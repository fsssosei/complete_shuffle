'''
complete_shuffle - This package is used to complete shuffle the list. 这个包用于对列表完全洗牌。
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

from typing import Final, Callable, Union, Tuple, Optional
from math import pi, e, ceil, log2
from gmpy2 import c_div as gmpy2_c_div, fac as gmpy2_fac, bit_mask as gmpy2_bit_mask
from pure_nrng_package import *
from pure_prng_package import pure_prng

__all__ = ['prng_type_tuple', 'default_prng_type', 'calculate_number_of_shuffles_required', 'tr_complete_shuffle', 'pr_complete_shuffle', 'tr_complete_cyclic_permutation', 'pr_complete_cyclic_permutation', 'tr_complete_derangement', 'pr_complete_derangement']

True_Randbits = Callable[[int], int]
Unbias = bool

prng_type_tuple: Final[tuple] = tuple(pure_prng.prng_type_list)
default_prng_type = pure_prng.default_prng_type

def _shuffle(x: list, randint: Callable[[int, int, bool, Optional[int]], int]) -> None:
    '''
        Shuffle list x in place, and return None.
        
        The formal parameter randint requires a callable object such as rand_int(b, a) that generates a random integer within the specified closed interval.
    '''
    for i in range(len(x) - 1, 0, -1):
        rand_int = randint(i)
        random_location = next(rand_int)
        x[i], x[random_location] = x[random_location], x[i]


def _random_cyclic_permutation(x: list, randint: Callable[[int, int, bool, Optional[int]], int]) -> None:
    '''
        Random cyclic permutation list x in place, and return None.
        
        The formal parameter randint requires a callable object such as rand_int(b, a) that generates a random integer within the specified closed interval.
    '''
    for i in range(len(x) - 1, 0, -1):
        rand_int = randint(i - 1)
        random_location = next(rand_int)
        x[i], x[random_location] = x[random_location], x[i]


def _random_derangement(x: list, randint: Callable[[int, int, bool, Optional[int]], int]) -> None:
    '''
        Random derangement list x in place, and return None.
        An element can never be in the same original position after the shuffle. provides uniform distribution over permutations.
         
        The formal parameter randint requires a callable object such as rand_int(b, a) that generates a random integer within the specified closed interval.
    '''
    x_length = len(x)
    if x_length > 1:
        for i in range(x_length):
            x[i] = {'sequence_number': i, 'elem': x[i]}
        
        end_label = x_length - 1
        while True:
            for i in range(end_label, 0, -1):
                rand_int = randint(i)
                random_location = next(rand_int)
                if x[random_location]['sequence_number'] != i:
                    x[i], x[random_location] = x[random_location], x[i]
                else:
                    break
            else:
                if x[0]['sequence_number'] != 0: break
        
        for i in range(x_length):
            x[i] = x[i]['elem']


def calculate_number_of_shuffles_required(item_number: int, formula_type: str, period: Optional[int] = None) -> int:
    '''
        The number of permutations of a list item is the factorial of the number of list items. The number of binary digits of the total number of permutations can be calculated by Stirling's formula.
        When the pseudo-random number algorithm used for shuffling is a variable period, the hash block size required for shuffling is calculated (equivalent to the period).
        Or when the number of pseudo-random number period used for shuffling is less than the number of permutations in the list, multiple shuffling is required. A shuffle is sufficient if the number of pseudo-random period multiplied by each shuffle is greater than the number of permutations in the list.
        
        Parameters
        ----------
        item_number: int
            The number of items to shuffle the list.  要洗牌列表的项数。
            item_number must be >= 1
        
        formula_type: str['prng_period' | 'shuffle_number']
            Set the computed result to be output according to pseudo-random period or shuffle number.
        
        period: int, default None
            Eigenperiod of a random number generator (maximum period)  随机数生成器的本征周期（最大周期）
            period must be >= 2
        
        Examples
        --------
        >>> calculate_number_of_shuffles_required(12, 'prng_period')
        288230376151711744
        >>> calculate_number_of_shuffles_required(1000, 'shuffle_number', 2 ** 256)
        67
    '''
    if item_number <= 160:  #Faster algorithms for small item_number values.
        bit_length_of_permutation_number = gmpy2_fac(item_number).bit_length()
    else:
        bit_length_of_permutation_number = ceil(log2(2 * pi * item_number) / 2 + log2(item_number / e) * item_number)
    
    if formula_type == 'prng_period':
        prng_period = 1 << (bit_length_of_permutation_number << 1)  #Any PRNG should have a period longer than the square of the number of outputs required.
        return prng_period
    elif formula_type == 'shuffle_number':
        shuffle_number = int(gmpy2_c_div(bit_length_of_permutation_number, (period - 1).bit_length() // 2))
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
    
    nrng_instance = pure_nrng(*true_randbits_args)
    randint = nrng_instance.true_rand_int
    _shuffle(x, randint)


def _dynamic_docstring_of_pr_complete_shuffle():
    pr_complete_shuffle.__doc__ = pr_complete_shuffle.__doc__.replace('{default_prng_type}', default_prng_type)
    pr_complete_shuffle.__doc__ = pr_complete_shuffle.__doc__.replace('{prng_type_tuple}', ', '.join([item for item in prng_type_tuple]))


def pr_complete_shuffle(x: list, seed: Optional[int] = None, prng_type: str = default_prng_type, additional_hash: Union[bool, Callable[[int, int], int], None] = None) -> None:
    '''
        Complete shuffle the list based on pseudo-random Numbers.
        
        Parameters
        ----------
        x: list
            The list of shuffles.
        
        seed: int, default None
            The seed of a non-negative integer value pseudo-random number generator.
            The default of None is to seed a random number generated by a system.
            The entropy of the seed must not be less than the number of permutations in the list.(Calculate with "calculate_number_of_shuffles_required" function)
        
        prng_type: str, default {default_prng_type}
            Specifies the pseudo-random number generator algorithm to use. 指定所用的伪随机数生成器算法。
            Available algorithms: {prng_type_tuple}
        
        additional_hash: bool, or Callable[[int, int], int]], default None
                Enable built-in security hashes to further confuse pseudo-random Numbers.  启用内置安全散列对伪随机数做进一步混淆。
                Or introduce an external hash function to accomplish this.  或引入外部散列函数完成此功能。
        
        Returns
        -------
        pr_complete_shuffle: None
            Instead of returning a value, this function directly modifies the content of the argument x.
        
        Examples
        --------
        >>> sequence_list = list(range(12))
        >>> prng_period = calculate_number_of_shuffles_required(12, 'prng_period')
        >>> seed = 170141183460469231731687303715884105727 & gmpy2_bit_mask((prng_period - 1).bit_length())
        >>> pr_complete_shuffle(sequence_list, seed)
        >>> sequence_list
        [6, 0, 9, 11, 2, 1, 7, 5, 3, 10, 4, 8]
    '''
    assert isinstance(x, list), f'x must be an list, got type {type(x).__name__}'
    
    list_len = len(x)
    if list_len > 1:
        algorithm_characteristics_parameter = pure_prng.prng_algorithms_dict[prng_type]
        
        if algorithm_characteristics_parameter['variable_period']:
            new_prng_period = calculate_number_of_shuffles_required(list_len, 'prng_period')
            prng_instance = pure_prng(seed, prng_type, new_prng_period, additional_hash)
            prng_instance_rand_int = prng_instance.rand_int
            _shuffle(x, prng_instance_rand_int)
        else:
            prng_period = algorithm_characteristics_parameter['prng_period']
            if prng_period != float('+inf'):
                shuffle_number = calculate_number_of_shuffles_required(list_len, 'shuffle_number', prng_period)
                if shuffle_number == 1:
                    prng_instance = pure_prng(seed, prng_type, additional_hash = additional_hash)
                    prng_instance_rand_int = prng_instance.rand_int
                    _shuffle(x, prng_instance_rand_int)
                else:
                    output_size = algorithm_characteristics_parameter['output_size']
                    output_mask = gmpy2_bit_mask(output_size)
                    seed = rng_util.randomness_extractor(seed, output_size * shuffle_number)
                    for i in range(shuffle_number):
                        sub_seed = (seed >> (output_size * i)) & output_mask
                        prng_instance = pure_prng(sub_seed, prng_type, additional_hash = additional_hash)
                        prng_instance_rand_int = prng_instance.rand_int
                        _shuffle(x, prng_instance_rand_int)
            else:
                prng_instance = pure_prng(seed, prng_type, additional_hash = additional_hash)
                prng_instance_rand_int = prng_instance.rand_int
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
    
    nrng_instance = pure_nrng(*true_randbits_args)
    randint = nrng_instance.true_rand_int
    _random_cyclic_permutation(x, randint)


def _dynamic_docstring_of_pr_complete_cyclic_permutation():
    pr_complete_cyclic_permutation.__doc__ = pr_complete_cyclic_permutation.__doc__.replace('{default_prng_type}', default_prng_type)
    pr_complete_cyclic_permutation.__doc__ = pr_complete_cyclic_permutation.__doc__.replace('{prng_type_tuple}', ', '.join([item for item in prng_type_tuple]))


def pr_complete_cyclic_permutation(x: list, seed: Optional[int] = None, prng_type: str = default_prng_type, additional_hash: Union[bool, Callable[[int, int], int], None] = None) -> None:
    '''
        Complete cyclic permutation the list based on pseudo-random Numbers.
        
        Parameters
        ----------
        x: list
            The list of random cyclic permutation.
        
        seed: int, default None
            The seed of a non-negative integer value pseudo-random number generator.
            The default of None is to seed a random number generated by a system.
            The entropy of the seed must not be less than the number of permutations in the list.(Calculate with "calculate_number_of_shuffles_required" function)
        
        prng_type: str, default {default_prng_type}
            Specifies the pseudo-random number generator algorithm to use. 指定所用的伪随机数生成器算法。
            Available algorithms: {prng_type_tuple}
        
        additional_hash: bool, or Callable[[int, int], int]], default None
                Enable built-in security hashes to further confuse pseudo-random Numbers.  启用内置安全散列对伪随机数做进一步混淆。
                Or introduce an external hash function to accomplish this.  或引入外部散列函数完成此功能。
        
        Returns
        -------
        pr_complete_cyclic_permutation: None
            Instead of returning a value, this function directly modifies the content of the argument x.
        
        Examples
        --------
        >>> sequence_list = list(range(12))
        >>> prng_period = calculate_number_of_shuffles_required(12, 'prng_period')
        >>> seed = 170141183460469231731687303715884105727 & gmpy2_bit_mask((prng_period - 1).bit_length())
        >>> pr_complete_cyclic_permutation(sequence_list, seed)
        >>> sequence_list
        [6, 11, 0, 9, 2, 1, 7, 5, 3, 10, 4, 8]
    '''
    assert isinstance(x, list), f'x must be an list, got type {type(x).__name__}'
    
    list_len = len(x)
    if list_len > 1:
        algorithm_characteristics_parameter = pure_prng.prng_algorithms_dict[prng_type]
        
        if algorithm_characteristics_parameter['variable_period']:
            new_prng_period = calculate_number_of_shuffles_required(list_len, 'prng_period')
            prng_instance = pure_prng(seed, prng_type, new_prng_period, additional_hash)
            prng_instance_rand_int = prng_instance.rand_int
            _random_cyclic_permutation(x, prng_instance_rand_int)
        else:
            prng_period = algorithm_characteristics_parameter['prng_period']
            if prng_period != float('+inf'):
                shuffle_number = calculate_number_of_shuffles_required(list_len, 'shuffle_number', prng_period)
                if shuffle_number == 1:
                    prng_instance = pure_prng(seed, prng_type, additional_hash = additional_hash)
                    prng_instance_rand_int = prng_instance.rand_int
                    _random_cyclic_permutation(x, prng_instance_rand_int)
                else:
                    output_size = algorithm_characteristics_parameter['output_size']
                    output_mask = gmpy2_bit_mask(output_size)
                    seed = rng_util.randomness_extractor(seed, output_size * shuffle_number)
                    for i in range(shuffle_number):
                        sub_seed = (seed >> (output_size * i)) & output_mask
                        prng_instance = pure_prng(sub_seed, prng_type, additional_hash = additional_hash)
                        prng_instance_rand_int = prng_instance.rand_int
                        _random_cyclic_permutation(x, prng_instance_rand_int)
            else:
                prng_instance = pure_prng(seed, prng_type, additional_hash = additional_hash)
                prng_instance_rand_int = prng_instance.rand_int
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
    
    nrng_instance = pure_nrng(*true_randbits_args)
    randint = nrng_instance.true_rand_int
    _random_derangement(x, randint)


def _dynamic_docstring_of_pr_complete_derangement():
    pr_complete_derangement.__doc__ = pr_complete_derangement.__doc__.replace('{default_prng_type}', default_prng_type)
    pr_complete_derangement.__doc__ = pr_complete_derangement.__doc__.replace('{prng_type_tuple}', ', '.join([item for item in prng_type_tuple]))


def pr_complete_derangement(x: list, seed: Optional[int] = None, prng_type: str = default_prng_type, additional_hash: Union[bool, Callable[[int, int], int], None] = None) -> None:
    '''
        Complete derangement the list based on pseudo-random Numbers.
        
        Parameters
        ----------
        x: list
            The list of random derangement.
        
        seed: int, default None
            The seed of a non-negative integer value pseudo-random number generator.
            The default of None is to seed a random number generated by a system.
            The entropy of the seed must not be less than the number of permutations in the list.(Calculate with "calculate_number_of_shuffles_required" function)
        
        prng_type: str, default {default_prng_type}
            Specifies the pseudo-random number generator algorithm to use. 指定所用的伪随机数生成器算法。
            Available algorithms: {prng_type_tuple}
        
        additional_hash: bool, or Callable[[int, int], int]], default None
                Enable built-in security hashes to further confuse pseudo-random Numbers.  启用内置安全散列对伪随机数做进一步混淆。
                Or introduce an external hash function to accomplish this.  或引入外部散列函数完成此功能。
        
        Returns
        -------
        pr_complete_derangement: None
            Instead of returning a value, this function directly modifies the content of the argument x.
        
        Note
        ----
        Can be used for lists with duplicate elements.
        
        Examples
        --------
        >>> sequence_list = list(range(12))
        >>> prng_period = calculate_number_of_shuffles_required(12, 'prng_period')
        >>> seed = 170141183460469231731687303715884105727 & gmpy2_bit_mask((prng_period - 1).bit_length())
        >>> pr_complete_derangement(sequence_list, seed)
        >>> sequence_list
        [6, 0, 9, 11, 2, 1, 7, 5, 3, 10, 4, 8]
    '''
    assert isinstance(x, list), f'x must be an list, got type {type(x).__name__}'
    
    list_len = len(x)
    if list_len > 1:
        algorithm_characteristics_parameter = pure_prng.prng_algorithms_dict[prng_type]
        
        if algorithm_characteristics_parameter['variable_period']:
            new_prng_period = calculate_number_of_shuffles_required(list_len, 'prng_period')
            prng_instance = pure_prng(seed, prng_type, new_prng_period, additional_hash)
            prng_instance_rand_int = prng_instance.rand_int
            _random_derangement(x, prng_instance_rand_int)
        else:
            prng_period = algorithm_characteristics_parameter['prng_period']
            if prng_period != float('+inf'):
                shuffle_number = calculate_number_of_shuffles_required(list_len, 'shuffle_number', prng_period)
                if shuffle_number == 1:
                    prng_instance = pure_prng(seed, prng_type, additional_hash = additional_hash)
                    prng_instance_rand_int = prng_instance.rand_int
                    _random_derangement(x, prng_instance_rand_int)
                else:
                    output_size = algorithm_characteristics_parameter['output_size']
                    output_mask = gmpy2_bit_mask(output_size)
                    seed = rng_util.randomness_extractor(seed, output_size * shuffle_number)
                    for i in range(shuffle_number):
                        sub_seed = (seed >> (output_size * i)) & output_mask
                        prng_instance = pure_prng(sub_seed, prng_type, additional_hash = additional_hash)
                        prng_instance_rand_int = prng_instance.rand_int
                        _random_derangement(x, prng_instance_rand_int)
            else:
                prng_instance = pure_prng(seed, prng_type, additional_hash = additional_hash)
                prng_instance_rand_int = prng_instance.rand_int
                _random_derangement(x, prng_instance_rand_int)
_dynamic_docstring_of_pr_complete_derangement()
