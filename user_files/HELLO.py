# def extract_primary_diagonal(matrix):
  # diagonal = [i[1] for i in matrix]
  #diagonal_sum = sum(diagonal)
  # return diagonal, diagonal_sum

#M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#diag, total = extract_primary_diagonal(M)
#print(f"Diagonal: {diag} | Sum: {total}")

#a, b = input("Enter two numbers: ").split()
#print(a+b)

#p = 2
#print(eval('2 * p - 1'))#

#print("Name: %s, Age: %d" % ("Alice", 8))
#print("Pi: %.2f" % 3.14159)
#print("Name: {1}, Age: {0}".format("Alice", 20))

#a=3
#b=4
#c=5
#x=a if a>=b and a>=c b elif b>=c and b>=c c else c>=b and c>=a
#print(x)

#=123214
#=list(str(x))
#rint(type(x))
#or i in x:
 #  print(i,end='')
  # print('*',end='')

#x=1234
#c=1
# x=str(x)
#for i in x:
 #   n=int(i)
  #  c*=n
#print(f"Product of digits :{c}")

#x=[1,2,3,4,5,6]
#pos=int(input("Enter pos: "))
#v=int(input("Entr val :"))
#c=len(x)
#n=[]
#for i in range(pos):
#    n+=[x[i]]
#n+=[v]
#for i in range(pos+1,c):
#    n+=[x[i]]
#print(f"New list : {n}")

#x=int(input("Enter no of terms in fibonnaci :"))
#c=0
#a,b=0,1
#while c<x:
 #   print(a,end=" ")
  #  a,b=b,a+b
   # c+=1

#x=int(input("Enter : "))
#if x<=1:
#    print("Not  prime ")
#else:
#    c=1
#    i=2
#    while i*i<=x:
#        if x%i==0:
#            c=0
#            break
#        i+=1
#
#    print("prime" if c==1 else"not prime")



#x=['a','b','a']
#y={}
#for i in x:
#   y[i]=y.get(i,0)+1
#for a,b in y.items():
#    print(f"ROLL NO :{a}  |  FREQ : {b}")


#=int(input("Enter input : "))
#or i in range(x+1):
#   for j in range(i):
#       print("*",end=' ')
# print()


#=[1,3,4,5]
#=[4,5,6,7,8,1,2,3]
#or i in x:
#   if i not in y:
#       y+=[i]
#rint(y)



# e=[x**2 if x%2==0 else x for x in range(1,10)]
#print(e)
 
"""
Multi-line comment (actually a docstring)
Used for longer explanations
print""hell")"""

'''x,y=map(float,input("Enter 2 val with space").split())
x,y=int(x),int(y)
z=[x,y]
print(z)'''

'''l=[1,2,3,4]
print(l.pop())'''

'''A = {"Aditi", "Bala", "Charan", "Deepak"}
B = {"Charan", "Deepak", "Esha", "Farhan"}
c=A.union(B)
d=A.intersection(B)
e=A.difference(B)
f=A.symmetric_difference(B)
print(f"uniion :{c} | intersection : {d} | diff : {e} | symm : {f}")'''

'''y=[2,3,4,5,6,7]
x=frozenset(y)
print(f"Frozenset : {x}")'''
  
'''x=("SENSOR_TEMP_01", "2026-11-05", 28.5, 29.1,28.8, 30.2, "OK")
a,b,*c,d=x
print(a,b,c,d)'''

'''
c="ababbabababdbjjhojiryyethwt"
x={}
for i in c:
    x[i]=x.get(i,0) + 1
print("the frequency is ", x)'''


'''x=(9,2,3,4,5)
print(sorted(x))'''


'''x=5
for i in range(x,0,-1):
    for j in range(i):
        print("*",end=" ")
    print()'''

'''x=5
for i in range(1,x+1):
    print("  " * (x-i),end=' ') 
    for j in range(i):
        print('*',end=' ')
    print() '''

'''x=10
for i in range(1,x+1):
    print(' ' * (x-i),end=' ')
    for j in range(i):
        print("*",end=' ')
    print()
for i in range(x-1,0,-1):
    print(" " * (x-i),end=' ')
    for j in range(i):
        print('*',end=' ')
    print()'''




'''for i in range(1, 11):
    for j in range(1, 11):
        print(f"{i*j:4d}", end=' ')
    print()'''


'''def make_order(customer, *items, **metadata):
    print(f"Customer:  {customer}")
    print(f"Items:  {items}")
    print(f"Metadata:  {metadata}")
make_order("Alice", "Pizza", "Coke", "Brownie", table=4, priority="High")'''

'''n=[1,2,3,44,56,2,123,4,5,6,7]
x=len(n)
for i in range(x):
    for  j in range(0,x-1-i):
        if n[j]>n[j+1]:
            n[j],n[j+1]=n[j+1],n[j]
print(n)'''


'''x=6
for i in range(x,0,-1):
    print(" " * (x-i),end=' ')
    for j in range(1,i+1):
        print(j,end=' ')
    print()'''

