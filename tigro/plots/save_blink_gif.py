import io

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def save_blink_gif(
    image1,
    image2,
    filename="blink.gif",
    interval=200,
    n_cycles=20,
    figsize=(8, 8),
    dpi=100,
    **imshow_kwargs,
):
    """
    Save two images as an animated GIF suitable for Google Slides.

    Parameters
    ----------
    image1, image2 : array-like
        Images accepted by matplotlib.pyplot.imshow.

    filename : str, default="blink.gif"
        Output GIF filename.

    interval : int or float, default=200
        Time between frames in milliseconds.

    n_cycles : int, default=20
        Number of blinking cycles stored in the GIF.

    figsize : tuple, default=(8, 8)
        Matplotlib figure size.

    dpi : int, default=100
        Resolution used to render each frame.

    **imshow_kwargs
        Additional arguments passed to imshow, e.g.
        cmap, vmin, vmax, interpolation, origin.
    """

    def render(image):
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
        ax.imshow(image, **imshow_kwargs)
        ax.axis("off")

        fig.subplots_adjust(
            left=0, right=1,
            bottom=0, top=1
        )

        buffer = io.BytesIO()
        fig.savefig(
            buffer,
            format="png",
            dpi=dpi,
            bbox_inches="tight",
            pad_inches=0,
        )
        plt.close(fig)

        buffer.seek(0)
        return Image.open(buffer).convert("RGB")

    frame1 = render(image1)
    frame2 = render(image2)

    frames = [frame1, frame2] * n_cycles

    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=interval,
        loop=0,
    )
