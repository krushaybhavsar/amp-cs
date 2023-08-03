import math


class ProjectEulerSolutions:
    def open_file(self, file_name, mode="r"):
        data_location = "project-euler\\data\\"
        return open(data_location + file_name, mode)

    def problem_1(self):
        sum = 0
        for i in range(1000):
            if i % 3 == 0 or i % 5 == 0:
                sum += i
        return sum

    def problem_2(self):
        fib = []
        i = 0
        while True:
            if i == 0 or i == 1:
                fib.append(1)
            else:
                fib.append(fib[i - 1] + fib[i - 2])
            i += 1
            if fib[-1] >= 4 * (10**6):
                break
        sum = 0
        for i in range(len(fib)):
            if fib[i] % 2 == 0:
                sum += fib[i]
        return sum

    def problem_3(self):
        num = 600851475143
        factors = []
        while num != 1:
            for i in range(2, num + 1, 1):
                if num % i == 0:
                    factors.append(i)
                    num = num // i
                    break
        return max(factors)

    def problem_7(self):
        prime_search_position = 10001
        primes = [2]
        n = 3
        while len(primes) != prime_search_position:
            possible_prime = n % 2 != 0
            for i in range(3, int(math.sqrt(n)) + 1, 2):
                if n % i == 0:
                    possible_prime = False
            if possible_prime:
                primes.append(n)
            n += 1
        return primes[prime_search_position - 1]

    def problem_10(self):
        sum = 2
        n = 3
        while n < 2 * (10**6):
            possible_prime = n % 2 != 0
            for i in range(3, int(math.sqrt(n)) + 1, 2):
                if n % i == 0:
                    possible_prime = False
            if possible_prime:
                sum += n
            n += 1
        return sum

    def problem_59(self):
        with self.open_file("0059_cipher.txt") as f:
            cipher = f.read().split(",")
        cipher = [int(i) for i in cipher]
        f = self.open_file("0059_cipher_messages.txt", "w")
        decrypted_msg_sum = 0
        for i in range(97, 123):  # a-z
            for j in range(97, 123):  # a-z
                for k in range(97, 123):  # a-z
                    key = [i, j, k]
                    message = []
                    for l in range(len(cipher)):
                        character = cipher[l] ^ key[l % 3]
                        message.append(character)
                    # filter messages that have weird characters or dont start with an english letter
                    if 127 not in message and (message[0] >= 65 and message[0] <= 90) or (message[0] >= 97 and message[0] <= 122):
                        message = "".join(chr(i) for i in message) + "\n" + str(sum(message)) + "\n\n"
                        f.write(message)
                        if "euler" in message.lower():  # found solution manually, extracting answer programmatically
                            decrypted_msg_sum = int(message.split("\n")[-3])

        f.close()
        return decrypted_msg_sum

    def run_solution(self, num):
        try:
            result = getattr(ProjectEulerSolutions(), f"problem_{num}")()
            print(f"\nThe solution to problem {num} is:\n{result}\n")
        except Exception as e:
            print(f"\nProblem {num} has not been solved yet!\n")
            print(f"Code failed with the following error:\n{e}\n")


if __name__ == "__main__":
    ProjectEulerSolutions().run_solution(59)
