import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import uuid

def download_images(url, save_folder):
    # Crear la carpeta si no existe
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Agregar un User-Agent para evitar bloqueos
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

    # Obtener el contenido de la página
    response = requests.get(url, headers=headers)

    # Verificar si la solicitud fue exitosa
    if response.status_code != 200:
        print(f"Error al acceder a la página: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todas las etiquetas <img>
    img_tags = soup.find_all('img')

    for img in img_tags:
        # Obtener la URL de la imagen (priorizando diferentes atributos)
        img_url = img.get('src') or img.get('data-src') or img.get('data-lazy-src') or img.get('srcset')

        if img_url:
            # Construir la URL completa
            img_url = urljoin(url, img_url)

            # Obtener la extensión del archivo
            parsed_url = urlparse(img_url)
            ext = os.path.splitext(parsed_url.path)[1]  # Obtener la extensión

            # Si no tiene extensión, asignar una por defecto
            if not ext:
                ext = ".jpg"

            # Crear un nombre único para evitar sobrescribir imágenes con nombres genéricos
            img_name = f"{uuid.uuid4().hex}{ext}"

            try:
                # Descargar la imagen
                img_data = requests.get(img_url, headers=headers, timeout=10).content

                # Guardar la imagen en la carpeta especificada
                with open(os.path.join(save_folder, img_name), 'wb') as img_file:
                    img_file.write(img_data)
                print(f'Imagen descargada: {img_name}')
            except Exception as e:
                print(f'Error al descargar {img_url}: {e}')
        else:
            print('No se encontró una URL válida para la imagen.')

if __name__ == '__main__':
    # URL del dominio que deseas rastrear
    domain_url = 'https://www.yalacanvaslodges.com/us/safari-tents/comet/'

    # Carpeta donde se guardarán las imágenes
    save_folder = 'downloaded_images'

    # Llamar a la función para descargar las imágenes
    download_images(domain_url, save_folder)
