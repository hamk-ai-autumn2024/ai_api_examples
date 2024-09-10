import io
import os
import math
from typing import Tuple
from PIL import Image
import urllib.request


def fetch_url(url: str) -> bytes:
    """
    Fetches the contents of the given URL and returns it as a bytes array.
    
    Args:
        url (str): The URL to fetch.
    
    Returns:
        bytes: The contents of the URL as a bytes array, or None if there are any errors.
    """
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None

def read_binary_file(filename: str) -> bytes:
    """
    Reads the contents of the given file and returns it as a bytes array.
    
    Args:
        filename (str): The filename to read.
    
    Returns:
        bytes: The contents of the file as a bytes array, or None if there are any errors.
    """
    try:
        with open(filename, "rb") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def save_binary_file(data: bytes, filename: str) -> bool:
    """
    Saves the given bytes array to a file with the given filename.
    
    Args:
        data (bytes): The data to save.
        filename (str): The filename to save the data to.
    
    Returns:
        bool: True if the file was successfully saved, False otherwise.
    """
    try:
        with open(filename, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def find_new_file_name(base_name: str) -> str:
    """
    Finds a new filename that doesn't already exist by adding a number to the end of the base name.
    Retains the file extension.

    Args:
        base_name (str): The base name to use.

    Returns:
        str: A new filename that doesn't already exist.
    """
    if not os.path.exists(base_name):
        return base_name

    i = 1
    while True:
        file_name, file_extension = os.path.splitext(base_name)
        new_name = f"{file_name}_{i}{file_extension}"
        if not os.path.exists(new_name):
            return new_name
        i += 1

def add_prefix_to_filename(filename: str, prefix: str) -> str:
    """
    Adds a prefix to the given filename, while retaining the file extension.

    Args:
        filename (str): The filename to add the prefix to.
        prefix (str): The prefix to add.

    Returns:
        str: The new filename with the prefix added.
    """
    path, file_name = os.path.split(filename)
    file_name, file_extension = os.path.splitext(file_name)
    new_name = os.path.join(path, f"{file_name}{prefix}{file_extension}")
    return new_name 

def find_aspect_ratio(width: int, height: int) -> str:
    """
    Finds the aspect ratio of an image given its width and height.
    
    Args:
        width (int): The width of the image.
        height (int): The height of the image.
    
    Returns:
        str: The aspect ratio of the image as a string in the format "width:height".
    """
    gcd = math.gcd(width, height)
    return f"{width // gcd}:{height // gcd}"

def find_image_file_dimensions(path: str) -> Tuple[int, int]:
    """
    Finds the dimensions of an image given its path.
    
    Args:
        path (str): The path to the image file.
    
    Returns:
        Tuple[int, int]: The width and height of the image.
    """
    with Image.open(path) as img:
        return img.size

def find_image_dimensions(data: bytes) -> Tuple[int, int]:
    """
    Finds the dimensions of an image given its binary data.
    
    Args:
        data (bytes): The binary data of the image.
    
    Returns:
        Tuple[int, int]: The width and height of the image.
    """
    with Image.open(io.BytesIO(data)) as img:
        return img.size
