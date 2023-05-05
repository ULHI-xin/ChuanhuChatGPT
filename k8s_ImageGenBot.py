import logging
import os
import sys

import colorama
import gradio as gr
import openai

from modules.image_gen_func import gen_image_from_prompt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
)

# NOTE: Hacky trick to change the behavior of Gallery.postprocess()
#       Otherwise the generated image urls will be prepended with {host/file=} and
#       now the file redirect is problematic with url parameters.
gr.Gallery.postprocess = lambda s, x: x


# if we are running in Docker
if os.environ.get("dockerrun") == "yes":
    dockerflag = True
else:
    dockerflag = False


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            prompt = gr.Textbox(label="Prompt", lines=4)
        with gr.Column():
            size_picker = gr.Dropdown(
                ['256x256', '512x512', '1024x1024'],
                value='512x512',
                label="Image Size",
                info="The size of the generated images. "
                     "Must be one of 256x256, 512x512, or 1024x1024."
                )
            n_slider = gr.Slider(
                1, 10, value=1, step=1,
                label="The number of images to generate. Must be between 1 and 10.")
    greet_btn = gr.Button("Generate")
    output = gr.Gallery(
        label="Generated images",
        show_label=False,
        elem_id="gallery"
    ).style(columns=(1, 2, 3, 4), object_fit="contain", height="auto")

    greet_btn.click(
        fn=gen_image_from_prompt,
        inputs=[prompt, size_picker, n_slider],
        outputs=output, api_name="gen_image_from_prompt")


if __name__ == "__main__":
    if not os.environ.get("my_api_key"):
        logging.error("Please give a api key!")
        sys.exit(1)

    openai.api_key = os.environ.get("my_api_key")
    _port = int(sys.argv[1])

    logging.info(
        colorama.Back.GREEN
        + f"\n Visit http://localhost:{_port}"
          f"\n OpenAI Image Generation: https://platform.openai.com/docs/guides/images/introduction"
        + colorama.Style.RESET_ALL
    )
    if dockerflag:
        demo.queue(concurrency_count=1).launch(
            server_name="0.0.0.0",
            server_port=_port,
            share=False,
            favicon_path="./assets/favicon.ico"
        )
    else:
        demo.queue(concurrency_count=1).launch(
            server_name="0.0.0.0",
            server_port=_port,
            share=False
        )
