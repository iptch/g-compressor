import azure.functions as func
import logging

app = func.FunctionApp()

@app.blob_trigger(arg_name="inputblob",
                  path="techcamp-source/{name}",
                  connection="AzureWebJobsStorage")
@app.blob_output(arg_name="outputblob",
                 path="techcamp-target-low/{name}",
                 connection="AzureWebJobsStorage")
def image_compressor(inputblob: func.InputStream, outputblob: func.Out[str]):
    logging.info(f"Python blob trigger function processed blob with name: {inputblob.name}")
    outputblob.set(inputblob.read())
