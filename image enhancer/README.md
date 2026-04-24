# AI Image Enhancer & Watermark Remover

A professional tool to enhance AI-generated images for use as high-resolution wallpapers.

## Features
- **Upscale to 4K**: Automatically scales images to 3840px (longest side) with high-quality resampling.
- **Watermark Removal**: 
  - **Crop**: Slices off the watermark area (User's preferred method).
  - **Inpaint**: Uses AI logic to fill the watermark area.
- **Visual Enhancement**: Sharpens and adjusts contrast for a premium look.
- **Batch Processing**: Select a folder and enhance multiple images at once.

## Installation
Ensure you have the required libraries:
```bash
pip install opencv-python numpy Pillow customtkinter
```

## Usage
Run the GUI:
```bash
python3 main.py
```

## File Structure
- `main.py`: The GUI application.
- `processor.py`: The image processing logic.
- `originals/`: Default folder for input images.
- `enhanced/`: Default folder for processed images.
