from PIL import Image, ImageFilter ,ImageOps, ImageChops, ImageDraw, ImageEnhance
import numpy as np
import os

# Load the image
image_path = 'C:\\Users\\kkhui\\CPII\\vintageFilter_py\\Sample.jpeg'
save_path = 'C:\\Users\\kkhui\\CPII\\vintageFilter_py\\result.jpg'
img = Image.open(image_path)

# res = img.convert("P",palette = Image.ADAPTIVE, colors = 8)
image = img.convert("P", colors=10)


pink_overlay = Image.new('RGB', image.size, (255, 182, 193))
res = Image.blend(image, pink_overlay, 0.2)  # Adjust the intensity as needed

# Step 3: Add grain (noise)
noise = np.random.randint(0, 100, (res.size[1], res.size[0], 3), dtype='uint8')
noise_image = Image.fromarray(noise, 'RGB')
res = Image.blend(res, noise_image, 0.2)  # Blend noise with the image


# Step 4: Reduce contrast
enhancer = ImageEnhance.Contrast(res)
res = enhancer.enhance(0.8)  # Lower contrast

# Display the image
res.show()
