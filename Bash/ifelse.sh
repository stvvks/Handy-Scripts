#!/bin/bash

# Example: Check if a variable is greater than 10

# Assign a value to the variable
my_variable=15

# Check the condition
if [ $my_variable -gt 10 ]; then
    echo "The variable is greater than 10."
else
    echo "The variable is not greater than 10."
fi


-----------------



#!/bin/bash

# Example: Check if a number is positive, negative, or zero

number=0

if [ $number -gt 0 ]; then
    echo "The number is positive."
elif [ $number -lt 0 ]; then
    echo "The number is negative."
else
    echo "The number is zero."
fi
