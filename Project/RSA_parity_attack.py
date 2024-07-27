# Import the necessary libraries for cryptographic operations and random number generation
import Crypto
from Crypto.Random import random
import Crypto.Random
from Crypto.Util.number import bytes_to_long, long_to_bytes
import random

class RSA:
    """Implements the RSA public key encryption / decryption."""

    def __init__(self, key_length):
        # Generate two large prime numbers, p and q, of the specified key_length
        self.p = Crypto.Util.number.getPrime(key_length)
        self.q = Crypto.Util.number.getPrime(key_length)
        # Calculate n = p * q
        self.n = self.p * self.q
        # Calculate the totient function phi(n) = (p-1)*(q-1)
        self.phi = (self.p - 1) * (self.q - 1)
        # Choose e such that 1 < e < phi(n) and gcd(e, phi(n)) = 1
        self.e = random.randint(1, self.phi)
        while Crypto.Util.number.GCD(self.e, self.phi) != 1:
            self.e += 1
        # Calculate d such that e * d ≡ 1 (mod phi(n))
        self.d = pow(self.e, -1, self.phi)

    def encrypt(self, binary_data):
        # Convert binary data to a long integer and encrypt it using the public key (e, n)
        return pow(bytes_to_long(binary_data), self.e, self.n)

    def decrypt(self, encrypted_int_data):
        # Decrypt the integer data using the private key (d, n) and convert it back to bytes
        return long_to_bytes(pow(encrypted_int_data, self.d, self.n)).decode()

class RSAParityOracle(RSA):
    """Extends the RSA class by adding a method to verify the parity of data."""

    def is_parity_odd(self, encrypted_int_data):
        # Decrypt the input data and return whether the resulting number is odd
        decrypted_int = pow(encrypted_int_data, self.d, self.n)
        return decrypted_int % 2 == 1

def parity_oracle_attack(ciphertext, rsa_parity_oracle):
    # Implement the attack and return the obtained plaintext
    l = 0 
    r = rsa_parity_oracle.n - 1
    power = pow(2, rsa_parity_oracle.e, rsa_parity_oracle.n)
    original_text = ciphertext
    while l < r:
        mid = (l + r) // 2
        ciphertext = (ciphertext * power) % rsa_parity_oracle.n
        if rsa_parity_oracle.is_parity_odd(ciphertext):
            l = mid + 1
        else:
            r = mid 
    l = l & (~0xff) # Align l to the nearest multiple of 256
    for i in range(0, 256):
        try:
            # Check if the modified value encrypts to the original ciphertext
            if (rsa_parity_oracle.encrypt(long_to_bytes(l + i)) == original_text):
                return long_to_bytes(l + i)
        except UnicodeDecodeError:
            pass

def main():
    input_bytes = input("Enter the message: ")

    # Generate a 1024-bit RSA pair    
    rsa_parity_oracle = RSAParityOracle(1024)

    # Encrypt the message
    ciphertext = rsa_parity_oracle.encrypt(input_bytes.encode())
    print("Encrypted message is: ", ciphertext)

    # Check if the attack works
    plaintext = parity_oracle_attack(ciphertext, rsa_parity_oracle)
    print("Obtained plaintext: ", plaintext)
    assert plaintext == input_bytes.encode()

if __name__ == '__main__':
    main()
