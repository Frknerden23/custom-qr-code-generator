# custom-qr-code-generator
A customizable Python desktop QR code generator with color customization, logo support, and PNG export using Tkinter, PyQRCode, and Pillow.

The application allows users to generate QR codes from URLs, customize foreground and background colors, optionally add a logo to the center of the QR code, and save the generated QR code as a PNG file.

🚀 Features

🔗 Generate QR codes from URLs
🎨 Customize foreground and background colors
🖼️ Add a custom logo to the center of the QR code
💾 Save QR codes as PNG files
⚡ High error correction level for logo-supported QR codes
🖥️ Simple and user-friendly desktop interface
❌ Error handling and user notifications

🛠️ Technologies

Python
Tkinter – Desktop GUI
PyQRCode – QR code generation
Pillow (PIL) – Image processing and logo integration
pypng – PNG generation support

📦 Installation

Clone the repository:



Install the required dependencies:

pip install pyqrcode pypng pillow

Run the application:

Logolu_qr.py

📖 How to Use
Enter the URL you want to convert into a QR code.
Select a foreground color.
Select a background color.
Optionally enable "Add logo" and choose an image.
Click "Generate QR Code".
Choose where you want to save the generated PNG file.

🖼️ Logo Support

The application uses the QR code's High Error Correction (H) level when a logo is added.

The logo is automatically resized and placed at the center of the QR code to maintain a balance between visual customization and QR readability.
