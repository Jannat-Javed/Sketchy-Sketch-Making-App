import cv2
import numpy as np
import streamlit as st
from PIL import Image
import io

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']

# Function to convert image to sketch
def make_sketch(img):
    grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(grayed)
    blurred = cv2.GaussianBlur(inverted, (21, 21), sigmaX=0, sigmaY=0)
    final_result = cv2.divide(grayed, 255 - blurred, scale=256)
    return final_result

# Streamlit app
st.set_page_config(page_title="Sketchy – Sketch Making App", layout="centered")
st.title("Sketchy – Sketch Making App")
st.write("Transform your images into beautiful sketches! Upload an image, and see the magic happen.")

# Add styling with custom CSS
st.markdown("""
    <style>
    .stButton>button {
        color: white;
        background-color: #4CAF50;
        border-radius: 8px;
        padding: 0.5em 1em;
        margin-top: 10px;
        font-size: 16px;
    }
    .stImage {
        border: 2px solid #4CAF50;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# File uploader for users to upload images
uploaded_file = st.file_uploader("Upload an image (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)

    # Display the original image
    with col1:
        original_image = Image.open(uploaded_file)
        st.image(original_image, caption="Original Image", use_column_width=True)

    # Convert to OpenCV format and create the sketch
    img = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)
    with st.spinner("Creating sketch... Please wait!"):
        sketch_img = make_sketch(img)

    # Convert the sketch to an image format compatible with Streamlit
    sketch_img_pil = Image.fromarray(sketch_img)

    # Display the sketch image
    with col2:
        st.image(sketch_img_pil, caption="Sketch Image", use_column_width=True)

    # Prepare image for download
    buf = io.BytesIO()
    sketch_img_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    # Add a download button
    st.download_button(
        label="Download Sketch Image",
        data=byte_im,
        file_name="sketch_image.png",
        mime="image/png",
        key='download-btn'
    )
else:
    st.info("Please upload an image to get started.")


