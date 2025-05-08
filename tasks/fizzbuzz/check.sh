#!/bin/bash
python3 -c "
from fizzbuzz import fizzbuzz
assert fizzbuzz(15)[-1] == 'FizzBuzz'
assert fizzbuzz(5) == ['1', '2', 'Fizz', '4', 'Buzz']
"
