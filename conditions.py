# if-else (example)
i = -4
# checking if i is greater than 0

if i > 0:
    print("i is positive")
    
else:
    print("i is 0 or negative")

age = 25
exp = 10


if age < 23 and exp > 8:
    print("Eligible")
    
    
else:
    print("Not Eligible")

# Nested if...else statement
i = 20

if i == 10:
    # first if statement
    if i > 15:
        print("i is smaller than 15")
    
    #nested if statement
    if i > 12:
        print("i is smaller than 12 too")
    else:
        print("i is greater than 15")
else:
        print("i is not equal to 10")


# if...elif...else


a = 5

#Checking if a is equal 10

if a == 10:
    print("a is equal to 10")
    

#Checking if a is equal 15
elif a == 15:
    print("a equals to 15")
    

#checking if a equals to 20
elif a == 20 :
    print("a equals to 20")
    
#If none of the above  conditions are true 
else:
    print("a is not present")
    
    
    
