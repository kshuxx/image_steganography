import cv2
import numpy as np
import gradio as gr
from cryptography.fernet import Fernet, InvalidToken
import base64
import hashlib

# Custom exception for steganography errors
class SteganographyException(Exception):
    pass

# Class for Least Significant Bit (LSB) Steganography
class LSBSteg():
    def __init__(self, im):
        self.image = im
        self.height, self.width, self.nbchannels = im.shape
        self.size = self.width * self.height

        # Masks for setting and clearing the least significant bit
        self.maskONEValues = [1, 2, 4, 8, 16, 32, 64, 128]
        self.maskONE = self.maskONEValues.pop(0)

        self.maskZEROValues = [254, 253, 251, 247, 239, 223, 191, 127]
        self.maskZERO = self.maskZEROValues.pop(0)

        self.curwidth = 0
        self.curheight = 0
        self.curchan = 0

    # Method to put binary value into the image
    def put_binary_value(self, bits):
        for c in bits:
            val = list(self.image[self.curheight, self.curwidth])
            if int(c) == 1:
                val[self.curchan] = int(val[self.curchan]) | self.maskONE
            else:
                val[self.curchan] = int(val[self.curchan]) & self.maskZERO

            self.image[self.curheight, self.curwidth] = tuple(val)
            self.next_slot()

    # Method to move to the next slot in the image
    def next_slot(self):
        if self.curchan == self.nbchannels - 1:
            self.curchan = 0
            if self.curwidth == self.width - 1:
                self.curwidth = 0
                if self.curheight == self.height - 1:
                    self.curheight = 0
                    if self.maskONE == 128:
                        raise SteganographyException("No available slot remaining (image filled)")
                    else:
                        self.maskONE = self.maskONEValues.pop(0)
                        self.maskZERO = self.maskZEROValues.pop(0)
                else:
                    self.curheight += 1
            else:
                self.curwidth += 1
        else:
            self.curchan += 1

    # Method to read a single bit from the image
    def read_bit(self):
        val = self.image[self.curheight, self.curwidth][self.curchan]
        val = int(val) & self.maskONE
        self.next_slot()
        if val > 0:
            return "1"
        else:
            return "0"

    # Method to read a byte (8 bits) from the image
    def read_byte(self):
        return self.read_bits(8)

    # Method to read a specified number of bits from the image
    def read_bits(self, nb):
        bits = ""
        for i in range(nb):
            bits += self.read_bit()
        return bits

    # Method to convert a value to its binary representation
    def byteValue(self, val):
        return self.binary_value(val, 8)

    # Method to convert a value to a binary string of a specified size
    def binary_value(self, val, bitsize):
        binval = bin(val)[2:]
        if len(binval) > bitsize:
            raise SteganographyException("binary value larger than the expected size")
        while len(binval) < bitsize:
            binval = "0" + binval
        return binval

    # Method to encode text into the image
    def encode_text(self, txt):
        txt = txt.encode('utf-8')  # Encode text to bytes
        l = len(txt)
        binl = self.binary_value(l, 32)  # Use 32 bits to store the length
        self.put_binary_value(binl)
        for byte in txt:
            self.put_binary_value(self.byteValue(byte))
        return self.image

    # Method to decode text from the image
    def decode_text(self):
        ls = self.read_bits(32)
        l = int(ls, 2)
        i = 0
        unhideTxt = bytearray()
        while i < l:
            tmp = self.read_byte()
            i += 1
            unhideTxt.append(int(tmp, 2))
        return unhideTxt.decode('utf-8')

# Function to generate a key from a password
def generate_key(password):
    # Use SHA-256 to hash the password and use it as a key
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

# Function to encrypt text with a password
def encrypt_text(text, password):
    key = generate_key(password)
    fernet = Fernet(key)
    encrypted_text = fernet.encrypt(text.encode())
    return encrypted_text

# Function to decrypt text with a password
def decrypt_text(encrypted_text, password):
    key = generate_key(password)
    fernet = Fernet(key)
    decrypted_text = fernet.decrypt(encrypted_text).decode()
    return decrypted_text

# Function to encode secret text into a carrier image with encryption
def encode_text_image(carrier_image, secret_text, password):
    encrypted_text = encrypt_text(secret_text, password)
    in_img = cv2.imread(carrier_image)
    steg = LSBSteg(in_img)
    res = steg.encode_text(encrypted_text.decode('utf-8'))
    output_image = "encoded_image.png"
    cv2.imwrite(output_image, res)
    return output_image

# Function to decode secret text from an encoded image with decryption
def decode_text_image(encoded_image, password):
    try:
        in_img = cv2.imread(encoded_image)
        steg = LSBSteg(in_img)
        encrypted_text = steg.decode_text()
        hidden_text = decrypt_text(encrypted_text.encode('utf-8'), password)
        return hidden_text
    except InvalidToken:
        return "Wrong password. Please try again."

# Gradio interface for encoding text into an image
encode_interface = gr.Interface(
    fn=encode_text_image,
    inputs=[
        gr.Image(type="filepath", label="Carrier Image"),
        gr.Textbox(label="Secret Text"),
        gr.Textbox(label="Password", type="password")
    ],
    outputs=gr.File(label="Download Encoded Image"),
    title="<h2 style='text-align: center;'>Encode Text into Image 🔐</h2>",
    description="Upload an image to serve as the carrier, input the secret message you wish to conceal,<br> and set a secure password. This process will encode your message into the image,<br> ensuring that only those with the correct password can decode and access the hidden text."
)

# Gradio interface for decoding text from an image
decode_interface = gr.Interface(
    fn=decode_text_image,
    inputs=[
        gr.Image(type="filepath", label="Encoded Image"),
        gr.Textbox(label="Password", type="password")
    ],
    outputs=gr.Textbox(label="Decoded Text"),
    title="<h2 style='text-align: center;'>Decode Text from Image 🔑</h2>",
    description="Upload an image that contains encoded text and enter the correct password to extract and reveal the hidden message.<br> This ensures that only authorized users with the correct password can access the concealed information"
)

# Launch the Gradio app with tabbed interfaces for encoding and decoding
app = gr.TabbedInterface([encode_interface, decode_interface], ["Encode", "Decode"], title="Image Steganography")
app.launch()
