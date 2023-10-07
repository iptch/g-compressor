import azure.functions as func
from PIL import Image
import io

def compress(inputblob: func.InputStream, resolution: int) -> bytes:
    image = Image.open(inputblob)

    # Set max height and width
    max_size = (resolution, resolution)

    # Create a thumbnail. This method modifies the image to contain 
    # a thumbnail version of itself, preserving original aspect ratio.
    image.thumbnail(max_size)

    # Save thumbnail to a BytesIO object
    output_stream = io.BytesIO()
    image.save(output_stream, format=image.format, quality=85)

    # Move back to the beginning of the stream
    output_stream.seek(0)

    return output_stream.read()
