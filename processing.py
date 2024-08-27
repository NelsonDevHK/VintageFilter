from PIL import Image, ImageFilter ,ImageOps, ImageChops, ImageDraw, ImageEnhance
import numpy as np
import glob
import os
from pathlib import Path
from setting import image_path,save_path

def process():
    img = Image.open(sample_path)

# res = img.convert("P",palette = Image.ADAPTIVE, colors = 8)
    image = img.convert("P", colors=10)
    # Step 1: Apply slight blur
    image = img.filter(ImageFilter.GaussianBlur(radius = 0.5))


#Step 2: chormatic effect
    r,g,b = image.split()

    r = ImageChops.offset(r, 2, 0)  # Move Red channel 5 pixels to the right
    g = ImageChops.offset(g, 0, 2)  # Move Green channel 5 pixels down
    b = ImageChops.offset(b, -2, 0) # Move Blue channel 5 pixels to the left

    res = Image.merge('RGB',(r,g,b))

    pink_overlay = Image.new('RGB', image.size, (255, 182, 193))
    res = Image.blend(res, pink_overlay, 0.2)  # Adjust the intensity as needed

# Step 3: Add grain (noise)
    noise = np.random.randint(0, 100, (res.size[1], res.size[0], 3), dtype='uint8')
    noise_image = Image.fromarray(noise, 'RGB')
    res = Image.blend(res, noise_image, 0.2)  # Blend noise with the image


# Step 4: Reduce contrast
    enhancer = ImageEnhance.Contrast(res)
    res = enhancer.enhance(0.8)  # Lower contrast
    return res


for sample_path in sorted(glob.glob(image_path + '/**/*.[jp][pn]g', recursive=True)):
    sample_id = Path(sample_path).stem
    output_dir = save_path / Path(sample_path).parent.relative_to(save_path)
    os.makedirs(str(output_dir), exist_ok=True)
    output_path = str(output_dir / (sample_id + Path(sample_path).suffix))
    if os.path.exists(output_path):
        continue
    res = process()

if res.mode == 'P' or res.mode == 'RBGA':
    res = res.convert('RGB')

res.save(save_path)
