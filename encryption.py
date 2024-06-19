#Creating a simple GUI registration form using Tkinter in Python  
#import the tkinter module into our code  
from tkinter import *  
from tkinter import messagebox
import numpy as np
import random

# Shift Cipher encryption 
def shift_cipher_encrypt(text, shift):
    result = ""
    for char in text:
        # Encrypt uppercase letters
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        # Encrypt lowercase letters
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char  # Leave non-alphabetical characters unchanged
    return result

# Caeser Cipher encryption   
def caeser_cipher_encrypt(text,shift):
    result = ""
    for char in text:
        # Encrypt uppercase letters
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        # Encrypt lowercase letters
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char  # Leave non-alphabetical characters unchanged
    return result
    
      
# Playfair Cipher encryption 
def prepare_text(text):
    # Remove non-alphabetical characters and convert to uppercase
    filtered_text = "".join(filter(str.isalpha, text.upper()))
    # Replace 'J' with 'I' (Playfair cipher does not use 'J')
    filtered_text = filtered_text.replace('J', 'I')

    # Split text into pairs of characters
    pairs = []
    i = 0
    while i < len(filtered_text):
        if i == len(filtered_text) - 1 or filtered_text[i] == filtered_text[i + 1]:
            pairs.append(filtered_text[i] + 'X')
            i += 1
        else:
            pairs.append(filtered_text[i] + filtered_text[i + 1])
            i += 2

    return pairs

def playfair_cipher_encrypt(text, key):
    # Prepare text for encryption
    pairs = prepare_text(text)
    
    # Create Playfair matrix based on the key
    matrix = []
    chars_in_key = []
    
    # Fill the key in the matrix
    for char in key.upper():
        if char not in chars_in_key and char.isalpha():
            chars_in_key.append(char)
    
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in alphabet:
        if char not in chars_in_key:
            chars_in_key.append(char)
    
    for i in range(5):
        matrix.append(chars_in_key[5 * i:5 * (i + 1)])

    # Encrypt pairs
    result = ""
    for pair in pairs:
        char1, char2 = pair[0], pair[1]
        row1, col1 = divmod(matrix.index([x for x in matrix if char1 in x][0]), 5)
        row2, col2 = divmod(matrix.index([x for x in matrix if char2 in x][0]), 5)

        if row1 == row2:
            result += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            result += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            result += matrix[row1][col2] + matrix[row2][col1]

    return result

# RailFence Cipher encryption 
def rail_fence_encrypt(text, key):
    rails = [''] * key
    direction = 1  # Direction for traversing the rails: 1 for down, -1 for up
    row = 0

    for char in text:
        rails[row] += char
        row += direction

        # Change direction when reaching the top or bottom rail
        if row == 0 or row == key - 1:
            direction = -direction

    # Concatenate all rail strings to form ciphertext
    result = ''.join(rails)
    return result

# Hill Cipher encryption
def hill_cipher_encrypt(text, key):
    # Clean the plaintext by removing non-alphabetic characters and converting to uppercase
    clean_text = ''.join(filter(str.isalpha, text.upper()))
    
    # Pad the text to make its length a multiple of the key matrix size
    while len(clean_text) % len(key) != 0:
        clean_text += 'X'
    
    # Generate numeric representation of the text
    numeric_text = [ord(char) - ord('A') for char in clean_text]
    
    # Generate key matrix
    try:
        key_matrix = np.array([[ord(char) - ord('A') for char in row.strip()] for row in key])
    except ValueError:
        messagebox.showerror("Error", "Invalid Hill Cipher key format. Use letters separated by commas.")
        return ""
    
    # Encrypt blocks of text with the key matrix
    result = ""
    for i in range(0, len(numeric_text), len(key)):
        block = np.array(numeric_text[i:i + len(key)])
        encrypted_block = np.dot(key_matrix, block) % 26
        result += ''.join([chr(num + ord('A')) for num in encrypted_block])
    
    return result

# Vernam Cipher Cipher encryption     
def otp_encrypt(text):
    # Generate a random key of the same length as the plaintext
    key = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(len(text)))
    
    # Perform XOR operation to encrypt
    result = ''.join(chr(ord(text[i]) ^ ord(key[i])) for i in range(len(text)))
    
    return result, key 


# Function to handle button click
def encrypt_text():
    plaintext = enter_1.get()
    technique = cv.get()
    encrypted_text = ""
    
    if technique == 'Shift':
        key = int(enter_3.get())
        encrypted_text = shift_cipher_encrypt(plaintext, key)
        
    elif technique == 'Caeser':
        key = enter_3.configure(state="disabled")
        encrypted_text = caeser_cipher_encrypt(plaintext, 3)
        
    elif technique == 'Playfair':
        key = enter_3.get()
        encrypted_text = playfair_cipher_encrypt(plaintext, key)
        
    elif technique == 'RailFence':
        key = int(enter_3.get())
        encrypted_text = rail_fence_encrypt(plaintext, key)
        
    elif technique == 'Hill':
        key = enter_3.get()
        encrypted_text = hill_cipher_encrypt(plaintext, key)
        
    elif technique == 'OTP':
        encrypted_text, key = otp_encrypt(plaintext)

    # Display encrypted text in the Cipher text label
    enter_5.delete(0, END)  # Clear previous text
    enter_5.insert(0, encrypted_text)

def reset_fields():
    enter_1.delete(0, END)
    enter_3.configure(state="normal")
    enter_3.delete(0, END)
    enter_5.delete(0, END)
    cv.set('--select--')
 

#Creating the object 'base' of the Tk()  
base = Tk()  
  
#Using the Geometry method to the form certain dimensions  
base.geometry("500x500")  
#Using title method to give the title to the window  
base.title('Cryptography')

label0 = Label(base, text="Encryption", width=20,font=("bold",20),fg='blue')  
label0.place(x=90,y=60)  

label1 = Label(base, text= "Plain text :", width=20,font=("bold",11))  
label1.place(x=80,y=130)  
   
enter_1 = Entry(base)  
enter_1.place(x=240,y=130) 

 
label4 =Label(base, text ="Technique :", width=20,font=("bold",11))  
label4.place(x=70,y=180)  
  
 
Techniques_of_encrypt =[ 'Shift' ,'Caeser','Playfair' , 'RailFence' ,'Hill' ,'OTP']  
  
cv = StringVar()  
drplist = OptionMenu(base, cv, *Techniques_of_encrypt)  
drplist.config(width=14)  
cv.set('--select--')  
drplist.place(x=240,y=180)
 
label3 = Label(base, text="Key :", width=20,font=("bold",11))  
label3.place(x=70,y=250)  
    
enter_3 = Entry(base)  
enter_3.place(x=240, y=250)  
    
Button(base, text='Convert' , width=20, bg="blue",fg='white', command=encrypt_text).place(x=100,y=300) 
Button(base, text='Reset' , width=20, bg="blue",fg='white' , command=reset_fields).place(x=280,y=300) 

label5 = Label(base, text= "Cipher text :", width=20,font=("bold",11))  
label5.place(x=80,y=380)  
  
enter_5 = Entry(base)  
enter_5.place(x=240,y=380)  
  
    
#Calling the mainloop method to execute the entire program.  
base.mainloop()  
