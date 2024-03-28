With the raising needs for faster and efficient data handling and deriving useful insights, we are extracting data from different types of sources. 
This application is designed to read the details provided in a business card, process them and store them in a database so that it can be retreived any time in the future.
The Approach:
  The image file stored in the local system is read with the EasyOCR library and the details are extracted in the for of a list.
  From it, the dta is processed to remove special characters and meaningful to be stored in a dataframe which is then written as separate columns in a MySQL table.
  The person's name, address, contact details, the path of the image of the card are also uploaded.
  The MySQL query to retreive the stored information is also provided.
