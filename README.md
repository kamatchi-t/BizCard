**Introduction**
    With the raising needs for faster and efficient data handling and deriving useful insights, we are extracting data from different types of sources. 
    This application is designed to read the details provided in a business card, process them and store them in a database so that it can be retreived any time in the future.
**The Approach**
  1. The image file stored in the local system is read with the EasyOCR library and the details are extracted in the for of a list.
  2. From it, the dta is processed to remove special characters and meaningful to be stored in a dataframe which is then written as separate columns in a MySQL table.
  3. The person's name, address, contact details, the path of the image of the card are also uploaded.
  4. The MySQL query to retreive the stored information is also provided.
**Libraries imported**
        1. import streamlit as st
        2. import pandas as pd
        3. import mysql.connector
        4. from PIL import Image
        5. import easyocr
        6. import imageio.v3 as iio
        7. from streamlit_extras.colored_header import colored_header
  
