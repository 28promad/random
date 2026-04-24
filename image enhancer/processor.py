import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import os

def enhance_image(input_path, output_path, target_long_side=3840, remove_watermark=True, removal_method='crop'):
    """
    Removes Gemini watermark, upscales to 4K equivalent, and enhances quality.
    """
    # 1. Load image with OpenCV
    img_cv = cv2.imread(input_path)
    if img_cv is None:
        raise ValueError(f"Could not read image: {input_path}")
    
    h, w = img_cv.shape[:2]
    
    # 2. Watermark Removal (Optional)
    if remove_watermark:
        # Based on Gemini images, watermark is in bottom right corner.
        # It usually takes up about 5-8% of height/width.
        margin_x = int(w * 0.08)
        margin_y = int(h * 0.08)

        if removal_method == 'crop':
            # Crop the right part to remove the watermark area
            # Keeping 'left side up until the watermark'
            img_cv = img_cv[:, :w-margin_x]
            h, w = img_cv.shape[:2] # Update dimensions after crop
        elif removal_method == 'inpaint':
            mask = np.zeros((h, w), dtype=np.uint8)
            cv2.rectangle(mask, (w - margin_x, h - margin_y), (w, h), 255, -1)
            img_cv = cv2.inpaint(img_cv, mask, 3, cv2.INPAINT_TELEA)
    
    # 3. Super-Resolution / Upscaling
    # Try to use AI Super-Resolution if model is available
    model_path = os.path.join(os.path.dirname(__file__), "models", "EDSR_x4.pb")
    ai_upscaled = False
    
    if os.path.exists(model_path):
        try:
            from cv2 import dnn_superres
            sr = dnn_superres.DnnSuperResImpl_create()
            sr.readModel(model_path)
            sr.setModel("edsr", 4)
            
            # AI upsample (EDSR x4)
            # This is slow but high quality
            img_cv = sr.upsample(img_cv)
            ai_upscaled = True
        except Exception as e:
            print(f"AI Upscaling failed, falling back to Lanczos: {e}")

    # Convert to RGB
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    
    # Calculate final dimensions
    h, w = img_cv.shape[:2]
    if w > h:
        new_w = target_long_side
        new_h = int(h * (target_long_side / w))
    else:
        new_h = target_long_side
        new_w = int(w * (target_long_side / h))
    
    # If AI upscaling didn't reach target or wasn't used, use LANCZOS
    if not ai_upscaled or (new_w != w or new_h != h):
        img_pil = img_pil.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 4. Visual Enhancements
    # Sharpening (more subtle if AI upscaled)
    if ai_upscaled:
        img_enhanced = img_pil.filter(ImageFilter.UnsharpMask(radius=1, percent=100, threshold=3))
    else:
        img_enhanced = img_pil.filter(ImageFilter.SHARPEN)
        img_enhanced = img_enhanced.filter(ImageFilter.DETAIL)
    
    # Contrast boost
    enhancer = ImageEnhance.Contrast(img_enhanced)
    img_enhanced = enhancer.enhance(1.1)
    
    # Saturation boost (subtle)
    enhancer = ImageEnhance.Color(img_enhanced)
    img_enhanced = enhancer.enhance(1.05)
    
    # 5. Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img_enhanced.save(output_path, quality=95, subsampling=0)
    
    return output_path

if __name__ == "__main__":
    # Test on one image
    test_input = "originals/Gemini_Generated_Image_5ydszw5ydszw5yds.png"
    test_output = "enhanced/test_output_crop.png"
    enhance_image(test_input, test_output, removal_method='crop')
    print(f"Test complete: {test_output}")
