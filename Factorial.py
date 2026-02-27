#Iterativo
def factorial (n):
    fact = 1

    for i in range (n):
        fact = i * fact
        return fact

print(factorial(1))

#Recursivo
def factorial_recursivo(n):
    n=1
    if n == 1:
        return 1
    
    else:
        return factorial_recursivo(n-1) * n

