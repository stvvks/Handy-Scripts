import os
import csv

#create a file w data in it

def create_file(filename):
    with open(filename, "w") as file:
        file.write("name,color,type\n")
        file.write("carnation,pink,annual\n")
        file.write("daffodil,yellow,perennial\n")
        file.write("iris,blue,perennial\n")

#read file, and format info of each row
def contents_of_file(filename):
    return_string = ""

#calling the function of creating file
    create_file(filename)

    #open file
    with open(filename) as file:
        #read rows of file into a dictionary
        reader = csv.DictReader(file)
        #process each item in dictionary
        for row in reader:
            return_string += "a {} {} is {}\n".format(
                row["color"], row["name"], row["type"])
    return return_string

    #Call function into a csv called flowers
    print(contents_of_file("flowers.csv"))
            


