import azure.functions as func
import logging
import compression
import os
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

@app.blob_trigger(arg_name="inputblob",
                  path="techcamp-source/{name}",
                  connection="AzureWebJobsStorage")
@app.blob_output(arg_name="outputblob",
                 path="techcamp-target-low/{name}",
                 connection="AzureWebJobsStorage")
def image_compressor_low(inputblob: func.InputStream, outputblob: func.Out[str]):
    logging.info(f"Python blob trigger function compressed image to LOW: {inputblob.name}")
    compressed_image = compression.compress(inputblob, 500)
    outputblob.set(compressed_image)

@app.blob_trigger(arg_name="inputblob",
                  path="techcamp-source/{name}",
                  connection="AzureWebJobsStorage")
@app.blob_output(arg_name="outputblob",
                 path="techcamp-target-ultra-low/{name}",
                 connection="AzureWebJobsStorage")
def image_compressor_ultra_low(inputblob: func.InputStream, outputblob: func.Out[str]):
    logging.info(f"Python blob trigger function compressed image to ULTRA LOW: {inputblob.name}")
    compressed_image = compression.compress(inputblob, 100)
    outputblob.set(compressed_image)

@app.event_grid_trigger(arg_name="azeventgrid")
def delete_compressed_image(azeventgrid: func.EventGridEvent):
    blob_name=os.path.basename(azeventgrid.subject)
    connection_string = os.environ["AzureWebJobsStorage"]
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    for container_name in ["techcamp-target-low", "techcamp-target-ultra-low"]:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.delete_blob()
