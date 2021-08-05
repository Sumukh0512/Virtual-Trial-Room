import os
import urllib.request
import time
import glob
import cv2
from app import app
from app2 import app2
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask_caching import Cache
import streamlit as st
from PIL import Image
from script import predict
#from evaluate import execute
#from pose_parser import pose_parse

#================ALLOWED FORMATS FOR IMAGE UPLOADS===========

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
cache = Cache()

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============ REDIRECT HOME PAGE==========================
	
@app.route('/')
def index():
	return render_template('index.html')
	
# ============ REDIRECT ABOUT PAGE=========================

@app.route('/about/')
def about():
	return render_template('about.html')	

# ============ REDIRECT SERVICE: TRY-ON====================

# ============ REDIRECT BLOG===============================
	
@app.route('/blog/')
def blog():
	return render_template('blog.html')

# ============ REDIRECT CONTACT===========================

@app.route('/contact/')
def contact():
	return render_template('contact.html')


# ================================================================================================================================================================
# ======================================================1. REDIRECT CASUALS ======================================================================================
@app.route('/casuals/')
def casuals():
	text = "none"
	fish = glob.glob('/output/TOM/val/try-on/*')
	for f in fish:
		os.remove(f)
	fish = glob.glob('./static/outputs/output_f/*')
	for f in fish:
		os.remove(f)
	cloth = ['001500','040404','606060','060606','050505','020202','030303','010101']
	#cloth = ['Casual-Yellow', 'Casual-Pink', 'Casual-Violet', 'Casual-White', 'Dark_ORANGE']
	for i in range(len(cloth)):
		cloth[i] = (str(cloth[i])+"_1.jpg")
	return render_template('casuals.html', casuals = cloth )

# ============1. FUNCTION TO DISPALY CASUALS =================

@app.route('/static/Database/val/cloth/')
def display_casuals(casuals):
	# time.wait(10)
	return send_from_directory(app2.config['OUTPUT_FOLDER2'], casuals)
	
# ============1. FUNCTION TO INPUT AND PROCESS TRY ON ==========

@app.route('/casual_form', methods=['POST'])
def upload_image():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	fish = glob.glob('/static/Database/val/image/*')
	for f in fish:
		os.remove(f)
	cloth = ['001500','040404','606060','060606','050505','020202','030303','010101']
	#cloth = ['Casual-Yellow', 'Casual-Pink', 'Casual-Violet', 'Casual-White', 'Dark_ORANGE', 'Flowers-White', 'Grey_North' , 'Light-Pink', 'Multicolo-White', 'Sky_Blue', 'TheNORTHface', 'Yellow62']	
	for i in range(len(cloth)):
		cloth[i] = (str(cloth[i])+"_1.jpg")

	if request.method=="POST":
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		
		text = "T103"
		file = request.files['file']		
		if file.filename == '':
			flash('No image selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename) and text:
			filename = secure_filename(file.filename)
			#file.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
			file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
			i_path = 'static/Database/val/image/'
			input_img = text+'.jpg'
			#os.rename(i_path+filename , i_path+input_img)
			filename = text+'.jpg'
			o_path = './output/TOM/val/try-on/'
			fish = glob.glob('./output/TOM/val/try-on/*')
			#fish = glob.glob('static/outputs/output_f/*')
			for f in fish:
				os.remove(f)
			time.sleep(10)
			#
			#
			#
			# 
			#pose_parse(text)
			#execute()
			valpair_file = 'static/Database/val_pairs.txt'
			
			for i in range(len(cloth)):
				with open(valpair_file , "w") as f:
						f.write(text+'.jpg '+ cloth[i] )
						f.close()
						predict()
						from PIL import Image
						im = Image.open("./output/TOM/val/try-on/"+input_img)
						#im = Image.open(os.path.join(o_path,cloth[i]))
						width, height = im.size
						left = 0
						top = 0
						right = width
						bottom = height-30
						im = im.crop((left, top, right, bottom)) 
						newsize = (200, 250) 
						im = im.resize(newsize)
						im.save(os.path.join(app2.config['OUTPUT_FOLDER3'],cloth[i]))
			#
			#
			#
			return render_template('casuals.html', casuals=cloth, text=text)
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	return render_template('casuals.html')

# =================1. OUTPUT CASUALS TRYON======================

@app.route('/static/outputs/output_f/<casuals>')
def display_output1(casuals):
	return send_from_directory(app2.config['OUTPUT_FOLDER3'], casuals)
	
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

