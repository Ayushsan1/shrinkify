import numpy as np
from PIL import Image
from django.shortcuts import render
from django.http import HttpResponse
import io
from sklearn.decomposition import PCA

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





def compress_image(image_path, n_components=50, output_path='compressed_image.jpg'):
    img = Image.open(image_path)
    img = img.convert('RGB')
    img_data = np.array(img)
    
 
    red_channel = img_data[:, :, 0]
    green_channel = img_data[:, :, 1]
    blue_channel = img_data[:, :, 2]
    
    def apply_pca(channel_data, n_components):
        pca = PCA(n_components=n_components, svd_solver='full')
        transformed_data = pca.fit_transform(channel_data)
        reconstructed_data = pca.inverse_transform(transformed_data)
        return reconstructed_data
    

    compressed_red = apply_pca(red_channel, min(n_components, red_channel.shape[1]))
    compressed_green = apply_pca(green_channel, min(n_components, green_channel.shape[1]))
    compressed_blue = apply_pca(blue_channel, min(n_components, blue_channel.shape[1]))
    
  
    compressed_img_data = np.stack((compressed_red, compressed_green, compressed_blue), axis=-1).astype(np.uint8)
    
   
    compressed_img = Image.fromarray(compressed_img_data)
    compressed_img.save(output_path)
    print(f"Compressed image saved at {output_path}")

compress_image('image_path provide kar yaha.jpg', n_components=50, output_path='output_image ka kya naam hona chahiye wo likh.jpg')
