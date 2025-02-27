import os
import cv2
import torch
import numpy as np
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from PIL import Image

# Configuración de modelos
CONTROLNET_MODEL_PATH = "lllyasviel/sd-controlnet-canny"
STABLE_DIFFUSION_MODEL_PATH = "runwayml/stable-diffusion-v1-5"

# Cargar ControlNet
controlnet = ControlNetModel.from_pretrained(CONTROLNET_MODEL_PATH, torch_dtype=torch.float16)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    STABLE_DIFFUSION_MODEL_PATH, 
    controlnet=controlnet,
    torch_dtype=torch.float16
).to("cuda")

# Función para preprocesar imagen (detección de bordes con Canny)
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(image, 100, 200)
    return Image.fromarray(edges)

# Carpeta de imágenes base
input_folder = "downloaded_images"
output_folder = "new_images"
os.makedirs(output_folder, exist_ok=True)

# Generar imágenes únicas
for img_file in os.listdir(input_folder):
    img_path = os.path.join(input_folder, img_file)
    
    # Procesar la imagen para extraer bordes
    canny_image = preprocess_image(img_path)

    # Generar imagen con Stable Diffusion
    generated_image = pipe(
        prompt="Imagen en alta calidad, estilo realista", 
        image=canny_image, 
        guidance_scale=7.5, 
        num_inference_steps=50
    ).images[0]
    
    # Guardar imagen generada
    output_path = os.path.join(output_folder, f"new_{img_file}")
    generated_image.save(output_path)
    print(f"Imagen generada: {output_path}")