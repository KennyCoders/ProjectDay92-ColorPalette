from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from PIL import Image
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                # Convert PIL Image to numpy array
                image = Image.open(file)
                img = np.array(image)
                # Save the uploaded image temporarily
                uploaded_image_path = os.path.join('static', 'uploads', file.filename)
                image.save(uploaded_image_path)
                # Update the image URL to point to the uploaded image
                image_url = uploaded_image_path
            else:
                # Use default image
                img = plt.imread('static/images/pic01.jpg')
                # Use default image URL
                image_url = 'static/images/pic01.jpg'
    else:
        # Use default image
        img = plt.imread('static/images/pic01.jpg')
        # Use default image URL
        image_url = 'static/images/pic01.jpg'

    red = img[:, :, 0]
    green = img[:, :, 1]
    blue = img[:, :, 2]

    # Flatten RGB matrix
    rgb_matrix = img.reshape(-1, 3)

    # Count occurrences of each color
    color_counts = Counter(map(tuple, rgb_matrix))

    # Get top 10 most used colors
    top_colors = color_counts.most_common(10)
    top_colors_rgb = [(list(color[0]), color[1]) for color in top_colors]

    # Render template with top 10 colors and image URL
    return render_template('index.html', top_colors=top_colors_rgb, image_url=image_url)


if __name__ == '__main__':
    app.run(debug=True)