# Image Steganography with LSB Technique 📷🔒

Welcome to the **Image Steganography** project! This project demonstrates how to hide secret messages within images using the Least Significant Bit (LSB) technique. 

## What is Steganography? 🤔

Steganography is the practice of concealing messages or information within other non-secret text or data. Unlike cryptography, which focuses on making the message unreadable to unauthorized parties, steganography aims to hide the very existence of the message.

## Least Significant Bit (LSB) Technique 🧩

The LSB technique is one of the simplest methods of steganography. It involves modifying the least significant bit of each pixel in an image. Since the change is minimal, it is generally imperceptible to the human eye.

### How It Works

1. **Encoding**: The secret message is converted into a binary format. Each bit of the message is then embedded into the least significant bit of the image pixels.
2. **Decoding**: The process is reversed to extract the hidden message from the image.

## Running the Application 🛠️

### Running Locally

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/image_steganography.git
cd image_steganography
pip install -r requirements.txt
```
Execute the following command:

```bash
python app.py
```

### Running on Google Colab

You can also run the project on Google Colab by clicking the link below:

[Run on Google Colab](https://colab.research.google.com/github/kshuxx/image_steganography/blob/main/image_steganography.ipynb)

## Usage 🛠️

### Encoding a Message

To encode a secret message into an image, use the `encode_text_image` function:

```python
import cv2
from steganography import encode_text_image

carrier_image = 'path/to/carrier_image.png'
secret_text = 'Your secret message here'

encoded_image = encode_text_image(carrier_image, secret_text)
print(f"Encoded image saved as {encoded_image}")
```

### Decoding a Message

To decode a secret message from an image, use the `decode_text_image` function:

```python
import cv2
from steganography import decode_text_image

encoded_image = 'path/to/encoded_image.png'

hidden_text = decode_text_image(encoded_image)
print(f"Hidden text: {hidden_text}")
```

## Gradio Interface 🌐

We have also provided a user-friendly web interface using Gradio. You can encode and decode messages directly from your browser.

### Launch the App

```python
import gradio as gr

# Gradio interface for encoding text into an image
encode_interface = gr.Interface(
    fn=encode_text_image,
    inputs=[
        gr.Image(type="filepath", label="Carrier Image"),
        gr.Textbox(label="Secret Text")
    ],
    outputs=gr.File(label="Download Encoded Image"),
    title="Encode Text into Image",
    description="Upload a carrier image and enter the secret text to encode the text into the image."
)

# Gradio interface for decoding text from an image
decode_interface = gr.Interface(
    fn=decode_text_image,
    inputs=gr.Image(type="filepath", label="Encoded Image"),
    outputs=gr.Textbox(label="Decoded Text"),
    title="Decode Text from Image",
    description="Upload an encoded image to extract the hidden text."
)

# Launch the Gradio app with tabbed interfaces for encoding and decoding
app = gr.TabbedInterface([encode_interface, decode_interface], ["Encode", "Decode"])
app.launch()
```

## Contributing 🤝

We welcome contributions! Please fork the repository and submit a pull request.

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.