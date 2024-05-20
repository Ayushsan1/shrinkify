import numpy as np
from PIL import Image
from django.shortcuts import render
from django.http import HttpResponse
import io

def index(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        compressed_image = compress_image(image)
        response = HttpResponse(content_type='image/jpeg')
        compressed_image.save(response, 'JPEG')
        response['Content-Disposition'] = 'attachment; filename="compressed.jpg"'
        return response
    else:
        return render(request, 'index.html')

def compress_image(image_file):
    # Load image
    image = Image.open(image_file)
    image = image.convert('L')  # Convert to grayscale
    image_data = np.asarray(image)

    # Perform PCA
    mean = np.mean(image_data, axis=0)
    centered_data = image_data - mean
    u, s, vh = np.linalg.svd(centered_data, full_matrices=False)
    k = 50  # Number of principal components to keep
    compressed_data = np.dot(u[:, :k], np.dot(np.diag(s[:k]), vh[:k, :]))
    compressed_data += mean
    compressed_data = np.clip(compressed_data, 0, 255).astype(np.uint8)

    # Create compressed image
    compressed_image = Image.fromarray(compressed_data)
    return compressed_image
