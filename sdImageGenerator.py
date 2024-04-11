import webuiapi
import uuid
from rembg import new_session, remove
from pathlib import Path

class SdImageGenerator:

    def __init__(self) -> None:
        #self.api = webuiapi.WebUIApi(baseurl=stableDiffusionUri)
        self.api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)

        #Set the model to be used by stable diffusion
        self.options = {}
        self.options['sd_model_checkpoint'] = "sdXL_v10VAEFix.safetensors [e6bb9ea85b]"

        #Set the model to be used for removing the background of the image
        self.session = new_session("isnet-anime")

        self.sdresults = "assets/img"
        self.nobackground = "assets/nb"
        Path(self.sdresults).mkdir(parents=True, exist_ok=True)
        Path(self.nobackground).mkdir(parents=True, exist_ok=True)

    def CreateImage(self, prompt):

        self.api.set_options(self.options)

        #Build the prompt
        prompt = f"mecha,dragon,(pokemon),black background,anime,cute,(({prompt}))"

        #create the character picture
        result = self.api.txt2img(prompt=prompt,
            negative_prompt="tiling,((out of frame)),body out of frame,((cut off)),low contrast,underexposed,overexposed,bad art,beginner,amateur,blurry,out of focus,portrait",
            cfg_scale=7,
            width=1024,
            height=1024,
            steps=40,
            save_images=True)
        
        #save the image to the sdresults folder
        filename = f"{uuid.uuid4()}.png"
        sdfilename = f"{self.sdresults}/{filename}"
        result.image.save(sdfilename, "PNG")

        #remove the background
        output_image = remove(result.image, session=self.session)

        #save the image to the nobackground folder
        nbfilename = f"{self.nobackground}/{filename}"
        output_image.save(nbfilename, "PNG")

        return output_image