a  = [1,2,3,4]
print(a[0:2])
print(a[::-1])
print(a[::3-1])
print(a[::2])

print(123%10)

a.pop()
print(a)
for i in a:
    print('i=',i)
    a.pop()
    for j in a:
        print('j=',j)
b = []
b.append(a)
sum([1,2,3])

a.append(1)
a.index(1)