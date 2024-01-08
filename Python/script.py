# Script that defines a value (which are 6 and 9) and spits out the other.
dict = {'6':'9', '9':'6'} #Using dict as a keypair to store values
print(dict.get(str(input("Enter 6 or 9: ")), "Incorrect number")) #Using print to spit out, str input allows the user to enter in a value and the opposite will be outputted