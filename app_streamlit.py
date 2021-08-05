import streamlit as st
from PIL import Image
from script import predict
import time
import os
from segmentation import run_pgn
#from test_pgn import PGN
#from evaluate import execute
from pose_parser import pose_parse
from image_mask import get_mask

st.title("Virtual Trial Room")
cloths = ['606060','020202','030303','707070','060606','13047','050505','040404','010101']
c = []
for i in range(len(cloths)):
	name = str(cloths[i]) + '_1.jpg'
	c.append(Image.open('static/Database/val/cloth/' + name))
slidebar = []
for i in range(len(c)):
	slidebar.append(st.sidebar.image(c[i], caption=str(cloths[i]), width=100, use_column_width=False))

dir="datasets/CIHP/image"
for f in os.listdir(dir):
    	os.remove(os.path.join(dir,f))

uploaded_person = st.file_uploader("Upload a Photo of size 192x256 (width*height) pixels", type="jpg")
#uploaded_person = st.file_uploader("Upload a Photo", type="jpg")
#st.write("Recommended: straight pose with background color-white")
user_input = st.text_input("Enter the User Name without space")
selected = st.selectbox('Select the Item Id:', ['','606060','020202','030303','707070','060606','13047','050505','040404','010101']
, format_func=lambda x: 'Select an option' if x == '' else x)
dir="static/Database/val/image-parse"
for f in os.listdir(dir):
    os.remove(os.path.join(dir,f))

if uploaded_person is not None and user_input is not '' and selected is not '':
    person = Image.open(uploaded_person)
    st.image(person, caption=user_input, width=100, use_column_width=False)
    st.write("Saving Image")
    bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.09)
        bar.progress(percent_complete + 1)
    person.save("static/Database/val/image/"+user_input+".jpg")
    person.save("datasets/CIHP/image/"+user_input+".jpg")
    progress1_bar=st.progress(0)
    st.write("Generating Image segmentation takes a minute!")
    #run_pgn()
    for percent_complete in range(100):
        time.sleep(0.05)
        progress1_bar.progress(percent_complete + 1)
    st.write("Please click the Try Button after Pose pairs and Masks are generated")
if st.button('Try'):
    st.write("Generating Mask and Pose Pairs")
    #PGN()
    run_pgn()
    pose_parse(user_input)
    get_mask()
    f = open("static/Database/val_pairs.txt" , "w")    
    f.write(user_input+".jpg "+selected+"_1.jpg")
    f.close()
    predict()
    from PIL import Image
    im = Image.open("./output/TOM/val/try-on/" + user_input + ".jpg")
    width, height = im.size  
  
# # Setting the points for cropped image  
    left = 0
    top = 0
    right = width
    bottom = height-30

  
# # Cropped image of above dimension  
# # (It will not change orginal image)  
    im1 = im.crop((left, top, right, bottom)) 
    newsize = (200,250)
    im1 = im1.resize(newsize) 
# # Shows the image in image viewer  
    im1.save("./output/TOM/val/try-on/" + user_input + ".jpg")
    execute_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.08)
        execute_bar.progress(percent_complete + 1)
    result = Image.open("./output/TOM/val/try-on/" + user_input + ".jpg")
    st.image(result , caption="Result" , width=200 , use_column_width=False)

## Super Reolution


