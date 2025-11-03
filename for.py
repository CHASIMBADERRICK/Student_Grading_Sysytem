# For  loop with String

s = ["python", "for", "programming", "This is handson practice"]

for i in s:
    print(i)
    
s = "python" 
for i in s:
    print(i)
    
#Using range() with the for loop   
for i in range(0, 11, 2):
    print(i)
    

# Control Statements with For Loop
# print all letters except 'n'  and 'm'
for a in "pythonforprogramming":
    if a == 'n' or a == 'm':
        continue
    print(a)


#Break statement   
for a in 'pythonprogramming':
     if a == 'n' or a == 'm':
         break
     print(a)
     
#Pass statement
for b in "pythonprogramming":
    pass
print(b)

#Else statetment with for loop

for i in range(1,4):
    print(i)
else:
    print('No Break\n')

#Using Enumerate with for 

a = ["code", "execute", "output", "input", "Display"]
for i, j in enumerate(a):
    print(i, j)


#Nested for loops
for i in range(1, 4):
    for j in range(1, 4):
        print(i, j)