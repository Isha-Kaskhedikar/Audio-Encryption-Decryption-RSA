from pydub import AudioSegment
import numpy as np 
from scipy.io.wavfile import read,write
import random
import matplotlib.pyplot as plt

#to verify prime number
def isPrime(num):
    if num > 1:
        for i in range(2, int(num/2)+1):
            if (num % i) == 0:
                return False
        else:
            return True
    else:
        return False

#to find gcd
def gcd(a,b):
    if(b==0):
        return a
    else:
        return gcd(b,a%b)

# function to produce encryption and decryption keys used in RSA algorithm      
def rsa(p,q):
    n=p*q  # first part of public key (n,e)
    phi = (p-1)*(q-1)
    k=5
    e=2

    while(e<phi):
        if gcd(e,phi)==1:
            break
        else:
            e+=1
    d=pow(e, -1, phi)#<------private key
    # public key = (n,e)
    # private key =(n,d)
    return [n,e,d]

# Function for encryption: 
# Formula: Encrypted Data c = (data)^e mod n. 
def encrypt(n,e,data):
    # print("input data:",(data))
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j]=(pow(data[i][j],e))%n
    # print("encrypted data:",(data))
    return data

# Function for decryption: 
# Formula: Decrypted Data = (c)^d mod n
def decrypt(n,d,data):
    datacopy=[]
    print("n,d:",(n,d))
    for i in range(len(data)):
        datacopy.append([(pow(int(data[i][0]),d))%n,(pow(int(data[i][1]),d))%n])
    # print("decrypted data:",(datacopy))
    return datacopy
    

#-------------MAIN--------------

#----------ENCRYPTION------------
data = read('tom.wav')
fs=data[0]
data = np.array(data[1],dtype=np.int16)

#prime numbers and encryption/decryption keys
primes = [i for i in range(10,30) if isPrime(i)] # generating 2 random prime numbers for RSA algorithm
pqlist=random.sample(primes, 2)
p=17
q=23

print("prime numbers: ",p,q)
lst=rsa(p,q)
n,e,d=lst[0],lst[1],lst[2]
# print(n,d)

# Call the encrypt function to encrypt the input data array and then convert it into a numpy array.
# Save the file in .wav format
encrypted_data=encrypt(n,e,data)
encrypted_data = np.asarray(encrypted_data,dtype=np.int16)

write('enc_data.wav',fs,encrypted_data)
plt.plot(encrypted_data)
plt.title("Encrypted Audio Plot")

# Save the encrypted data in .mp3 format and play it
sound = AudioSegment.from_wav('enc_data.wav')
wavfile=sound.export('enc_data.mp3', format='mp3')

#----------DECRYPTION------------

fsn,encrypted_wav=read('enc_data.wav')

decrypted_data=decrypt(n,d,encrypted_wav)

decrypted_data = np.asarray(decrypted_data,dtype=np.int16)
write('dec_data.wav',fsn,decrypted_data*100)
sound = AudioSegment.from_wav('dec_data.wav')
wavfile=sound.export('dec_data.mp3', format='mp3')