import mysql.connector 

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    database="csci314"
)
cursor = conn.cursor()

# Read image files and insert image data into the database
image_paths = ['visualex/static/images/cat_or_dog_1.jpg', 'visualex/static/images/cat_or_dog_2.jpg']
for image_path in image_paths:
    with open(image_path, 'rb') as file:
        image_data = file.read()
        # Insert image data into image_metadata table
        cursor.execute("INSERT INTO image_metadata (image_data) VALUES (%s)", (image_data,))

# Commit changes and close connection
conn.commit()
conn.close()
