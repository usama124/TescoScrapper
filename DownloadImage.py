## Importing Necessary Modules
import requests, base64  # to get image from the web
import shutil  # to save it locally


def download_image(image_url, filename):
    try:
        if "http" not in image_url:
            # Separate the metadata from the image data
            head, data = image_url.split(',', 1)

            # Get the file extension (gif, jpeg, png)
            file_ext = head.split(';')[0].split('/')[1]

            # Decode the image data
            plain_data = base64.b64decode(data)
            filename = "images/" + filename + "." + file_ext
            # Write the image to a file
            with open(filename, 'wb') as f:
                f.write(plain_data)
        else:
            # Open the url image, set stream to True, this will return the stream content.
            r = requests.get(image_url, stream=True)

            # Check if the image was retrieved successfully
            if r.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True
                img_ext = r.headers["Content-Type"].split("/")[-1]
                filename = "images/" + filename + "." + img_ext
                # Open a local file with wb ( write binary ) permission.
                with open(filename, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

                print('Image sucessfully Downloaded: ', filename)
            else:
                print('Image Couldn\'t be retreived' + image_url)
        return filename
    except Exception as e:
        print(e)
        return ""

#download_image("data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==", "img1")