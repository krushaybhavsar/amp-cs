import math

def to_binary_bin(n):
    #Approach #1: Built-in function: bin
    binary = bin(n)  
    binary = binary[2:] #creates a new string with spots [0] and [1] (ie. '0b') sliced off
    return binary
   
def to_binary_format(n):
    #Approach #2: Built-in function: format
    binary = format(n, 'b')
    return binary

def to_binary_divide(n):
    #Approach #3: Repeated division by 2
    binary = ""
    if n == 0: return "0"
    while n > 0:
        binary = str(n % 2) + binary
        n = n // 2
    return binary

def to_binary_subtract(n):
    #Approach #4: Repeated subtraction by powers of 2
    if n == 0: return "0"

    power_of_2 = math.floor(math.log2(n))
    binary = ""
    while power_of_2 >= 0:
        if n >= 2**power_of_2:
            binary = binary + "1"
            n = n - 2**power_of_2
        else:
            binary = binary + "0"
        
        power_of_2 = power_of_2 - 1
    
    return binary

def to_binary_bitwise(n):
    #Approach #5: Bitwise operators... assumes access to binary version of n, but returns a binary string
    #Corecting mistakes in this is an optional challenge... 
    binary = ""
    if n == 0: return "0"
    
    while n > 0:
        binary = str(n&1) + binary
        n = n >> 1
      
    return binary

if __name__ == '__main__':
    n = 0 #Only correct for non-negative integers... 

    print(to_binary_bin(n))
    print(to_binary_format(n))
    print(to_binary_divide(n))
    print(to_binary_subtract(n))
    print(to_binary_bitwise(n))