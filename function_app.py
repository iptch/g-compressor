import azure.functions as func
import logging
import compression
import os
from azure.storage.blob import BlobServiceClient

CONNECTION = "AzureWebJobsStorage"
SOURCE_CONTAINER = "techcamp-source"
TARGET_CONTAINER_LOW = "techcamp-target-low"
TARGET_CONTAINER_ULTRA_LOW = "techcamp-target-ultra-low"

app = func.FunctionApp()

@app.blob_trigger(arg_name="inputblob",
                  path=SOURCE_CONTAINER + "/{name}",
                  connection=CONNECTION)
@app.blob_output(arg_name="outputblob",
                 path=TARGET_CONTAINER_LOW + "/{name}",
                 connection=CONNECTION)
def image_compressor_low(inputblob: func.InputStream, outputblob: func.Out[str]):
    logging.info(f"Compressing '{inputblob.name}' to LOW")
    compressed_image = compression.compress(inputblob, 500)
    outputblob.set(compressed_image)

@app.blob_trigger(arg_name="inputblob",
                  path=SOURCE_CONTAINER + "/{name}",
                  connection=CONNECTION)
@app.blob_output(arg_name="outputblob",
                 path=TARGET_CONTAINER_ULTRA_LOW + "/{name}",
                 connection=CONNECTION)
def image_compressor_ultra_low(inputblob: func.InputStream, outputblob: func.Out[str]):
    logging.info(f"Compressing '{inputblob.name}' to ULTRA LOW")
    compressed_image = compression.compress(inputblob, 100)
    outputblob.set(compressed_image)

@app.event_grid_trigger(arg_name="azeventgrid")
def delete_compressed_image(azeventgrid: func.EventGridEvent):
    blob_name=os.path.basename(azeventgrid.subject)
    connection_string = os.environ[CONNECTION]
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    for container_name in [TARGET_CONTAINER_LOW, TARGET_CONTAINER_ULTRA_LOW]:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        if blob_client.exists():
            blob_client.delete_blob()
