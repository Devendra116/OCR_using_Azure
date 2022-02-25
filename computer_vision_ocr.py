import os
import io
import json,time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image ,ImageDraw,ImageFont

credentials=json.load(open('credentials.json'))
API_KEY=credentials['API_KEY']
ENDPOINT=credentials['ENDPOINT']

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))
read_image_url = "https://eoibrasilia.gov.in/photogalleryphp/p19470.jpg"

print("Reading the data here :")
# Call API with URL and raw response (allows you to get the operation location)
read_response = computervision_client.read(read_image_url,  raw=True)
# print(read_response)
# Get the operation location (URL with an ID at the end) from the response
read_operation_location = read_response.headers["Operation-Location"]
# Grab the ID from the URL
operation_id = read_operation_location.split("/")[-1]
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text, line by line
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            # print(line.bounding_box)
print()