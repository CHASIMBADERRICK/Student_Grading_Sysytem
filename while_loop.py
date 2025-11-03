#while loop synthax
# while expression
#     statement

# count = 0
# while count < 3:
#     count = count + 1
#     print("Programming")
    

# Infinite While loop in Python
# age = 20
# while age > 9:
#     print("infinite loop")

#continue statement
#Print letters except 'n' and 'm'
# i = 0
# a = 'pythonprogramming'

# while i < len(a):
#     if a[i] == 'n' or a[i] == 'm':
        
#         i += 1
#         continue
#     print(a[i])
#     i += 1

#Break Statement
# i = 0
# a = 'pythonprogramming'

# while i < len(a):
#     if  a[i] == 'n' or a[i] == 'm':
#         i += 1
#         break
#     print(a[i])
#     i += 1

#While loop  with pass statement
# a = 'pythonprogramming'
# i = 0

# while i < len(a):
#     i += 1
#     pass
# print('value of i :', i)

# While loop with else
i = 0
while i < 5:
    i += 1
    print(i)
    
else:
    print("No Break\n")
    
i = 0
while i > 5:
    i += 1
    print(i)
    break
else:
    print("No Break")
    