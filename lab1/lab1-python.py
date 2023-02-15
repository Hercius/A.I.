


def compute_difference(a,b):
    ''' returns the difference of a and b'''
    ## you fill this in
    return a-b

def reverse_string(s):
    '''reverse a string, e.g., reverse_string('abcd') returns 'dcba'''
    ## you fill this in
    return s [::-1]
def drop_odds(L):
    ''' remove the odd numbers from the list L, e.g., drop_odds([1,2,3,4]) returns [2,4]'''
    ## you fill this in
    for i in L:
        if i % 2 == 1:
            L.remove(i)
    return L
def birth_to_age(years):
    '''convert a list of birth years to a list of ages (assume all actual
birthdays are in February or later), e.g.,
birth_to_age([1997,1985,1999,1962]) returns [21,33,19,56]'''
    ## you fill this in
    age = years
    years[:] = [2020 - i for i in years]
    return age
def fibonacci(i):
    '''compute the i-th Fibonacci number: F[i] = F[i-2] + F[i-1], F[0] = F[1] = 1'''
    ## you fill this in
    count = 0
    for f in range(i,0,-1):
        count = count + f
    return count + 1

        
def square(n):
    '''print out an nxn square using '*' characters, e.g., square(3):
***
***
***
   '''
    ## you fill this in
    for i in range (0, n):
        for j in range(0, n):
            print("*", end=" ")
        print()
    
def distinct(L):
    '''return True if all elements of list L are unique, otherwise return
False if at least one element is repeated. '''
    ## you fill this in
    unique = []
    unique.append(L[0])
    for i in L:
        if i not in unique:
            unique.append(i)
    if len(L) == len(unique):
        return True
    if len(L) != len(unique):
        return False

def main():
    print("compute difference test (5-3): ")
    print(compute_difference(5,3))
    print("reverse string test (Computer): ")
    print(reverse_string("Computer"))
    print("drop odds test (1,2,3,4,5): ")
    print(drop_odds([1,2,3,4,5]))
    print("birth to age test (1998,1999,2000):")
    print(birth_to_age([1998,1999,2000]))
    print("fibonacci test (1) and then (4)")
    print(fibonacci(1))
    print (fibonacci(4))
    print("square test (4)")
    square(4)
    print("distinct test (1,1,2,2) then (1,2,3):")
    print(distinct([1,1,2,2]))
    print(distinct([1,2,3]))

if __name__ == '__main__':
    main()

