import streamlit as st
import io
import requests
import json
from PIL import Image
from PIL import ImageDraw

st.title('顔認識アプリ')

subscription_key = '08b7d892fe354c32bfadaa17cdbba3c1'
assert subscription_key

face_api_url = 'https://210208sayotoku.cognitiveservices.azure.com/face/v1.0/detect' 


uploaded_file =st.file_uploader('Choose an image...', type='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img.save(output, format='JPEG')
        binary_img = output.getvalue() #バイナリ取得

    headers = {
        'Content-Type':'application/octet-stream',    
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    } 
    res = requests.post(face_api_url, params=params,headers=headers, data=binary_img)   

    results = res.json()
    for result in results:
        rect = result['faceRectangle']
        age   = result['faceAttributes']['age']
        gender= result['faceAttributes']['gender']
    
        draw = ImageDraw.Draw(img) 
        draw.rectangle([(rect['left'],rect['top']), (rect['left'] + rect['width'], rect['top']+rect['height'])], fill=None, outline='green', width =3 )
    
        draw_x=rect['left']-5
        draw_y=rect['top']-15  
        text = gender + ',' + str(age)
        draw.text((draw_x, draw_y), text ,fill='red')

    st.image(img, caption='Uploaded Image.' , use_column_width=True)

