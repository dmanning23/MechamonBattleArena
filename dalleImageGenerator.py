from openai import OpenAI
import uuid
from rembg import new_session, remove
import base64
from io import BytesIO
from PIL import Image

class DalleImageGenerator:

    def CreateImage(self, prompt):

        #Set the model to be used for removing the background of the image
        #session = new_session("u2net")
        session = new_session("isnet-anime")

        #Create the image of the monster
        client = OpenAI()
        response = client.images.generate(
            #model="dall-e-3",
            model="dall-e-2",
            prompt=f"a mecha dragon in the style of Pokemon, based on the following prompt: {prompt}",
            #size="1024x1024",
            size="512x512",
            quality="standard",
            response_format="b64_json",
            n=1)

        #convert image to file-like object
        im_b64 = base64.b64decode(response.data[0].b64_json)
        img = Image.open(BytesIO(im_b64))

        #save to a file
        filename = f"{uuid.uuid4()}.png"
        sdfilename = f"assets/img/{filename}"
        img.save(sdfilename, "PNG")

        #remove the background
        output_image = remove(img, session=session)

        #save the image to the nobackground folder
        nbfilename = f"assets/nb/{filename}"
        output_image.save(nbfilename, "PNG")

        return output_image