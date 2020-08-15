import os
from PIL import Image
from db.DataAccessObject import DataAccessObject

PARENT = r"E:/data/grayscale/"
_CONVERT = False

# Initialize connection to database.
face_meta_coll = DataAccessObject(database="local", collection="faceData")
grayscale_coll = DataAccessObject(database="local", collection="grayscale")

# Convert to 64x64 8-bit grayscale
if _CONVERT:
    for path in os.listdir("E:/data/full"):
        img = Image.open("E:/data/full/" + path)
        gimg = img.convert("L")
        gimg.thumbnail((64, 64), Image.ANTIALIAS)
        gimg.save("E:/data/grayscale/" + path)

# Pull out all pixels and store with labels
face_meta_raw = face_meta_coll.get_num_image(20000)

for image_meta in face_meta_raw:
    # Format image path and open it.
    image_path = image_meta["images"][0]["path"]
    image_full_path = PARENT + image_path[5:]
    if not os.path.exists(image_full_path):
        continue
    image_core = Image.open(image_full_path)
    width, height = image_core.size
    pixels = [image_core.getpixel((j, i)) if image_core.getpixel((j, i)) != 255 else 0 for i in range(height) for j in range(width)]
    # Aggregate result as a document in new collection.
    new_doc = {
        "pixels": pixels,
        "gender": image_meta["gender"][0],
        "age": image_meta["age"][0],
        "ethnicity": image_meta["ethnicity"][0],
        "eye_color": image_meta["eye_color"][0],
        "hair_color": image_meta["hair_color"][0],
        "hair_length": image_meta["hair_length"][0],
        "emotion": image_meta["emotion"][0]
    }

    grayscale_coll.collection.insert_one(new_doc)
