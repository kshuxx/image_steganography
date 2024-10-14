# Image Steganography with LSB Technique 📷🔒

Welcome to the Image Steganography project! The program uses the Least Significant Bit (LSB) method to hide information within images. This technique ensures that the hidden data is imperceptible to the human eye, making it an effective method for securely embedding secret messages. Whether you are looking to protect sensitive information or simply explore the fascinating world of steganography.

## What is Steganography? 🤔

Steganography is the practice of concealing messages or information within other non-secret text or data. Unlike cryptography, which focuses on making the message unreadable to unauthorized parties, steganography aims to hide the very existence of the message.

## Least Significant Bit (LSB) Technique 🧩

The LSB technique is one of the easiest ways to hide information in images. Each color pixel in an image is made up of red, green, and blue parts, each stored in one byte. The idea is to hide information in the least significant bit (the smallest bit) of each color part of the pixel. This tiny change is usually not noticeable to the human eye. If there isn't enough space to hide all the information in the least significant bit, the program will start using the second least significant bit, and so on. However, the more data you hide, the easier it becomes to detect.

### LSBSteg module 🛠️

The LSBSteg module uses OpenCV to hide data in images. It works by storing information in the first bit of every pixel's color. If the first bit is full, it moves to the second bit. The program can hide all the data as long as there is enough space in the image.

Inspired by the work of  [RobinDavid/LSB-Steganography](https://github.com/RobinDavid/LSB-Steganography).

### How It Works

1. **Encoding**: The secret message is converted into a binary format. Each bit of the message is then embedded into the least significant bit of the image pixels. This process ensures that the visual changes to the image are minimal and not noticeable to the human eye.

2. **Decoding**: The process is reversed to extract the hidden message from the image. By reading the least significant bits of each pixel, the binary data is reconstructed and converted back into the original message.

## Running the Application ⚙️

### Running Locally

Clone the repository and install the required dependencies:s

```bash
git clone https://github.com/yourusername/image_steganography.git
```

```bash
cd image_steganography
```

```bash
pip install -r requirements.txt
```

Execute the following command:

```bash
python app.py
```

### Run on web 📡

You can also run the project on:

[![Run on Hugging Face](https://go-skill-icons.vercel.app/api/icons?i=huggingface)](https://kshuxx-image-steganography.hf.space)

## Gradio Interface 🌐

We have also provided a user-friendly web interface using Gradio. You can encode and decode messages directly from your browser. The interface is intuitive and easy to use, making it accessible even for those who are not familiar with coding. Simply upload your image, enter the text you want to hide or reveal, and let the application do the rest. This feature ensures that you can securely encode and decode messages.

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
