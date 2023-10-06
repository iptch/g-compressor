import azure.functions as func
import logging
from PIL import Image
import io

app = func.FunctionApp()

@app.blob_trigger(arg_name="inputblob",
                  path="techcamp-source/{name}.{extension}",
                  connection="AzureWebJobsStorage")
@app.blob_output(arg_name="outputblob",
                 path="techcamp-target-low/{name}.{extension}",
                 connection="AzureWebJobsStorage")
def image_compressor(inputblob: func.InputStream, outputblob: func.Out[str]):
    logging.info(f"Python blob trigger function processed blob with name: {inputblob.name}")

    image = Image.open(inputblob)
    print(f"Image format: {image.format}")

    max_size = (100, 100)

    # Create a thumbnail. This method modifies the image to contain 
    # a thumbnail version of itself, preserving original aspect ratio.
    image.thumbnail(max_size)

    # Save thumbnail to a BytesIO object
    output_stream = io.BytesIO()
    image.save(output_stream, format=image.format)

    # Move back to the beginning of the stream
    output_stream.seek(0)

    # Write the stream to blob storage
    outputblob.set(output_stream.read())
