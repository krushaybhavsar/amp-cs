import math
from TimingProfiler import TimingProfiler

def get_factors(n: int) -> list[int]:
    '''
    Generates a sorted list of unique integer factors for a given integer

    Args:
    n (int): The integer which should be factored

    Returns:
    list: a list of unique integer factors in sorted order

    Examples:

    >>>get_factors(17)
    [1, 17]
    >>>get_factors(36)
    [1, 2, 3, 4, 6, 9, 12, 18, 36]
    >>>get_factors(-2)
    []
    
    '''
    factors = [i for i in range(1, n + 1) if n % i == 0]
    return sorted(factors)

def is_prime_exhaustive(n: int) -> bool:
    if n < 2:
        return False
    factors = [i for i in range(2, n) if n % i == 0]
    return len(factors) == 0

def is_prime_exhaustive_escape(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def is_prime_skip_evens(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, n, 2):
        if n % i == 0:
            return False
    return True

def is_prime_skip_impossible_factors(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n))+1, 2):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    algorithms = [is_prime_exhaustive, is_prime_exhaustive_escape, is_prime_skip_evens, is_prime_skip_impossible_factors]
    test_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    # Local Testing: get_factors
    n = int(input("Enter a positive integer: "))

    factors = get_factors(n)
    print(f"The factors of {n} are {factors}")
    if len(factors) == 2:
        print(f"{n} is a prime number.")
    else:
        print(f"{n} is not a prime number.")

    # Verifying Correctness- is_prime
    for is_prime_algorithm in algorithms:
        actual_primes = []
        for n in range(101):
            if is_prime_algorithm(n):
                actual_primes.append(n)
        
        if test_primes == actual_primes:
            print(f"{is_prime_algorithm.__name__} correctly finds the primes less than or equal to 100")
        else:
            print(f"{is_prime_algorithm.__name__} has a mistake!!")
            print(f"  - Expected: {test_primes}")
            print(f"  - Actual: {actual_primes}")


    # Speed comparisons- is_prime
    inputs = [11, 101, 1009, 10007, 100003, 1000003, 10000019]
    trials = 10

    experiment = TimingProfiler(algorithms, inputs, trials)
    experiment.run_experiments()
    print(experiment.results)
    experiment.graph(title="is_prime Timings", scale="log")
