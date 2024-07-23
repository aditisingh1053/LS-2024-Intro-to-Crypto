import numpy as np

# This function converts the set of 3 alphabets into the ciphered tect by multiplying it by them
def hill_cipher_encrypt(key_matrix, plaintext):
    n = key_matrix.shape[0]
    plaintext_vector = [ord(char) - ord('a') for char in plaintext]
    ciphertext_vector = np.dot(key_matrix, plaintext_vector) % 26
    ciphertext = ''.join(chr(num + ord('a')) for num in ciphertext_vector)
    return ciphertext
# This whole cell for inputting the key
print("Enter a  3-digit key")
c=input()
key=c.lower().strip()
if len(key) != 9 or not key.isalpha():
    print("Enter 9 valid characters! Invalid input.")
    exit()
key_numbers = [ord(char) - ord('a') for char in key] #Converting the key into numbers
key_matrix = np.array(key_numbers).reshape(3, 3) # Converting into a matrix
# print(key_matrix)
print("Enter the input-text")
myvar=input()
input_text=myvar.lower().strip().split()

finalstring="" # this will store the string without anyy spaces so that they be ignored
for i in input_text:
    finalstring+=i
ciphertext = ""
if len(finalstring)%3!=0: # for padding
    for i in range (3-len(finalstring)%3):
        finalstring+='x'
# print(finalstring)
for i in range(0, len(finalstring), 3):
    block = finalstring[i:i+3] #Giving 3 3 alphabets to the function
    ciphertext += hill_cipher_encrypt(key_matrix, block)
    
print("Ciphertext:", ciphertext.upper())