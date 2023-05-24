import json


response = '''{
    "message": "Success",
    "result": [
        {
            "message": "Success",
            "input": "document_5.jpg",
            "prediction": [
                {
                    "id": "7485cfab-a1df-49a9-9119-9120f941d126",
                    "label": "Surname",
                    "xmin": 463,
                    "ymin": 175,
                    "xmax": 630,
                    "ymax": 203,
                    "score": 0.9298641,
                    "ocr_text": "STEVENS",
                    "type": "field",
                    "status": "correctly_predicted",
                    "page_no": 0,
                    "label_id": "9f7a436b-838e-44a7-93b3-bf99af974fd8"
                },
                {
                    "id": "602106cb-c088-4b93-adc3-cfac9e084127",
                    "label": "First_Name",
                    "xmin": 462,
                    "ymin": 267,
                    "xmax": 586,
                    "ymax": 295,
                    "score": 0.69895613,
                    "ocr_text": "ICHIKA",
                    "type": "field",
                    "status": "correctly_predicted",
                    "page_no": 0,
                    "label_id": "88f2f230-2e3d-441c-af2d-2f6795d294c5"
                },
                {
                    "id": "5fbf38f5-a761-40c5-89f4-c2122c9c3080",
                    "label": "Nationality",
                    "xmin": 460,
                    "ymin": 459,
                    "xmax": 565,
                    "ymax": 491,
                    "score": 0.55693436,
                    "ocr_text": "Japan",
                    "type": "field",
                    "status": "correctly_predicted",
                    "page_no": 0,
                    "label_id": "03d9e25d-7b1f-4321-95b4-15a9cb12d735"
                },
                {
                    "id": "a0f24c0d-c26f-4b0d-a40c-19dc387b6217",
                    "label": "Date_of_Birth",
                    "xmin": 463,
                    "ymin": 545,
                    "xmax": 685,
                    "ymax": 582,
                    "score": 0.9993083,
                    "ocr_text": "18 AUG 1988",
                    "type": "field",
                    "status": "correctly_predicted",
                    "page_no": 0,
                    "label_id": "b3f83958-a5b5-4d38-8d1c-322584d001f3"
                },
                {
                    "id": "d1dcc863-f532-4288-894e-54985e115329",
                    "label": "Sex",
                    "xmin": 740,
                    "ymin": 552,
                    "xmax": 762,
                    "ymax": 578,
                    "score": 0.97166777,
                    "ocr_text": "F",
                    "type": "field",
                    "status": "correctly_predicted",
                    "page_no": 0,
                    "label_id": "e68ade1e-aec1-4d6b-901b-5299ca4c7564"
                },
                {
                    "id": "9a9eb26d-fcf2-46f3-809e-b64a6cb7218e",
                    "label": "Date_of_expiry",
                    "xmin": 740,
                    "ymin": 603,
                    "xmax": 943,
                    "ymax": 628,
                    "score": 0.98851144,
                    "ocr_text": "07/04/2027",
                    "type": "field",
                    "status": "correctly_predicted",
                    "page_no": 0,
                    "label_id": "7135ea81-d39f-449b-bec8-70cc7a01bacc"
                }
            ],
            "page": 0,
            "request_file_id": "08e65700-f3b2-4d35-b874-d205aba9ba6f",
            "filepath": "uploadedfiles/ceeebab1-5f48-4ce9-845e-066b81ce3d97/PredictionImages/9ccbc21c-088f-4dd5-a3b1-a6c69616bcf0.jpeg",
            "id": "699d41f2-f952-11ed-9d08-ae80855f0ce2",
            "rotation": 0,
            "file_url": "uploadedfiles/ceeebab1-5f48-4ce9-845e-066b81ce3d97/RawPredictions/08e65700-f3b2-4d35-b874-d205aba9ba6f.jpg",
            "request_metadata": "",
            "processing_type": "sync"
        }
    ],
    "signed_urls": {
        "uploadedfiles/ceeebab1-5f48-4ce9-845e-066b81ce3d97/PredictionImages/9ccbc21c-088f-4dd5-a3b1-a6c69616bcf0.jpeg": {
            "original": "https://nnts.imgix.net/uploadedfiles/ceeebab1-5f48-4ce9-845e-066b81ce3d97/PredictionImages/9ccbc21c-088f-4dd5-a3b1-a6c69616bcf0.jpeg?expires=1684851197\u0026or=0\u0026s=87ca70a4b2b89e9b8278bd21beb89029",
            "original_compressed": "https://nnts.imgix.net/uploadedfiles/ceeebab1-5f48-4ce9-845e-066b81ce3d97/PredictionImages/9ccbc21c-088f-4dd5-a3b1-a6c69616bcf0.jpeg?auto=compress\u0026expires=1684851197\u0026or=0\u0026s=84391a6bd6455cc1f6f0fcbd8307d3d0",
            "thumbnail": "https://nnts.imgix.net/uploadedfiles/ceeebab1-5f48-4ce9-845e-066b81ce3d97/PredictionImages/9ccbc21c-088f-4dd5-a3b1-a6c69616bcf0.jpeg?auto=compress\u0026expires=1684851197\u0026w=240\u0026s=73d1035f975caaad9585b575f9c02a2c",
            "acw_rotate_90": "https://nnts.imgix.net/uploadedfiles/ceeebab1-5f48-4ce9-845e-066b81ce3d97/PredictionImages/9ccbc21c-088f-4dd5-a3b1-a6c69616bcf0.jpeg?auto=compress\u0026expires=1684851197\u0026or=270\u0026s=8f5aac4381773f78dd9f0040d5619e6d",
            "acw_rotate_180": "https://nnts.imgix.net/uploadedfiles/ceeebab1-5f48-4ce9-845e-066b81ce3d97/PredictionImages/9ccbc21c-088f-4dd5-a3b1-a6c69616bcf0.jpeg?auto=compress\u0026expires=1684851197\u0026or=180\u0026s=80e589e894764e1bcd8a6c8475ce7346",
            "acw_rotate_270": "https://nnts.imgix.net/uploadedfiles/ceeebab1-5f48-4ce9-845e-066b81ce3d97/PredictionImages/9ccbc21c-088f-4dd5-a3b1-a6c69616bcf0.jpeg?auto=compress\u0026expires=1684851197\u0026or=90\u0026s=96c607ae7e1ca89c9e2abb40b3ab1212",
            "original_with_long_expiry": "https://nnts.imgix.net/uploadedfiles/ceeebab1-5f48-4ce9-845e-066b81ce3d97/PredictionImages/9ccbc21c-088f-4dd5-a3b1-a6c69616bcf0.jpeg?expires=1700388797\u0026or=0\u0026s=e66ee94af30262e7f86e5fcf74d8155f"
        },
        "uploadedfiles/ceeebab1-5f48-4ce9-845e-066b81ce3d97/RawPredictions/08e65700-f3b2-4d35-b874-d205aba9ba6f.jpg": {
            "original": "https://nanonets.s3.us-west-2.amazonaws.com/uploadedfiles/ceeebab1-5f48-4ce9-845e-066b81ce3d97/RawPredictions/08e65700-f3b2-4d35-b874-d205aba9ba6f.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256\u0026X-Amz-Credential=AKIA5F4WPNNTLX3QHN4W%2F20230523%2Fus-west-2%2Fs3%2Faws4_request\u0026X-Amz-Date=20230523T101317Z\u0026X-Amz-Expires=604800\u0026X-Amz-SignedHeaders=host\u0026response-cache-control=no-cache\u0026X-Amz-Signature=0997982241fa2fc33d3a371112dba7bb2e44f972b571ef140b8f50406facd5e5",
            "original_compressed": "",
            "thumbnail": "",
            "acw_rotate_90": "",
            "acw_rotate_180": "",
            "acw_rotate_270": "",
            "original_with_long_expiry": ""
        }
    }
}'''


data = json.loads(response)

filtered_data = []
for item in data['result'][0]['prediction']:
    filtered_item = {item['label']: item['ocr_text']}
    filtered_data.append(filtered_item)
    

print(filtered_data)


