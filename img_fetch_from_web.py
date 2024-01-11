# Import libraries
import os
import requests
from requests.exceptions import InvalidSchema
from bs4 import BeautifulSoup
from is_img_support_by_tf import is_image_supported

# base url
base_url = "https://unsplash.com/s/photos/trucks"

def soup(url: str) -> BeautifulSoup:
    # Fetch the page contents
    content: bytes = requests.get(
                    url,
                    timeout = 5
                    ).content
    
    return BeautifulSoup(
        content, 
        "html.parser"
        )

def download_imgs(
            bs: BeautifulSoup,
            path: str
            ):
    # Select the all images on the pages
    images = bs.select("img")
    
    # Create a directory
    if not os.path.exists(path):
        os.mkdir(path)
    
    # Loop over the images
    for idx, img in enumerate(images):
        # Get the image source link
        links = img.get("src")
        
        try:
            # Get the image content
            contents = requests.get(
                    links,
                    timeout = 5
                ).content
            if len(path) == 0:
                raise ValueError("Path must be filled  but it's a empty string")
            image_path = f"{path}/img-{idx}.jpeg"
            with open(image_path, "wb") as f:
                f.write(contents)

            # Check if the image is support by tensorflow
            if not is_image_supported(image_path):
                os.remove(image_path)
                
        except (FileExistsError, InvalidSchema):
            continue

    print("All images have been downloaded ")  
        
        
bs4 = soup(base_url)
#print(bs4.prettify())
download_imgs(bs4, "vehicles")
        
