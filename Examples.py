a = [1,3,5, 7, 9,11]
val = 7

for i in a:
    if i == val:
        print(f"Found at {i}!")
        break
    
    else:
        print("Not found")


for i in range(15):
    print(i)
    if i == 8:
        break


count = 5
while True:
    print(count)
    count -= 1
    if count == 0:
        print("Count if Finished")
        
        break
    

matrix = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    [10,11,12]
]

val = 6
found = False

for r in matrix:
    for n in r:
        if n == val:
            print(f"{val} found")
            
            found = True
            break
        if  found:
            break