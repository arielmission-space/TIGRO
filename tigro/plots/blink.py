import base64
import io
import uuid

import matplotlib.pyplot as plt
from IPython.display import HTML, display
from PIL import Image

def blink(
    image1,
    image2,
    interval=200,
    n_cycles=None,
    titles=("Image 1", "Image 2"),
    figsize=(8, 8),
    **imshow_kwargs,
):
    """
    Blink between two images entirely in the notebook browser.

    The images are rendered once by Matplotlib. JavaScript then alternates
    between the two resulting PNG images without further communication with
    the Python kernel.

    Parameters
    ----------
    image1, image2 : array-like
        Images accepted by matplotlib.pyplot.imshow.

    interval : int or float, default=200
        Time between image changes, in milliseconds.

    n_cycles : int or None, default=None
        Number of complete image1/image2 cycles. If None, blink indefinitely.

    titles : tuple of str, default=("Image 1", "Image 2")
        Labels shown above the images.

    figsize : tuple of float, default=(8, 8)
        Figure size used when rendering each image.

    **imshow_kwargs
        Additional arguments passed to imshow, such as cmap, vmin, vmax,
        origin, interpolation, and extent.
    """

    def image_to_png_data(image):
        fig, ax = plt.subplots(figsize=figsize)
        ax.imshow(image, **imshow_kwargs)
        ax.axis("off")
        fig.tight_layout(pad=0)

        buffer = io.BytesIO()
        fig.savefig(
            buffer,
            format="png",
            bbox_inches="tight",
            pad_inches=0,
        )
        plt.close(fig)

        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
        return f"data:image/png;base64,{encoded}"

    source1 = image_to_png_data(image1)
    source2 = image_to_png_data(image2)

    widget_id = f"blink_{uuid.uuid4().hex}"
    max_changes = "null" if n_cycles is None else str(2 * n_cycles)

    html = f"""
    <div id="{widget_id}" style="display:inline-block; text-align:center;">
        <div class="blink-title"
             style="font-weight:600; margin-bottom:6px;">
            {titles[0]}
        </div>

        <img class="blink-image"
             src="{source1}"
             style="max-width:100%; display:block;">

        <div style="margin-top:8px;">
            <button class="blink-toggle">Pause</button>
            <button class="blink-next" style="display:none;">Next</button>
            <button class="blink-reset">Restart</button>
        </div>
    </div>

    <script>
    (() => {{
        const root = document.getElementById("{widget_id}");
        const image = root.querySelector(".blink-image");
        const title = root.querySelector(".blink-title");

        const toggleButton = root.querySelector(".blink-toggle");
        const nextButton = root.querySelector(".blink-next");
        const resetButton = root.querySelector(".blink-reset");

        const sources = [
            {source1!r},
            {source2!r}
        ];

        const titles = [
            {titles[0]!r},
            {titles[1]!r}
        ];

        const interval = {float(interval)};
        const maxChanges = {max_changes};

        let frame = 0;
        let changes = 0;
        let timer = null;

        function showFrame(index) {{
            frame = index;
            image.src = sources[frame];
            title.textContent = titles[frame];
        }}

        function advanceFrame() {{
            showFrame(1 - frame);
            changes += 1;

            if (maxChanges !== null && changes >= maxChanges) {{
                stop();
                return false;
            }}

            return true;
        }}

        function step() {{
            advanceFrame();
        }}

        function start() {{
            if (timer !== null) return;

            if (maxChanges !== null && changes >= maxChanges) {{
                changes = 0;
                showFrame(0);
            }}

            timer = window.setInterval(step, interval);

            toggleButton.textContent = "Pause";
            nextButton.style.display = "none";
        }}

        function stop() {{
            if (timer !== null) {{
                window.clearInterval(timer);
                timer = null;
            }}

            toggleButton.textContent = "Play";
            nextButton.style.display = "inline-block";
        }}

        toggleButton.addEventListener("click", () => {{
            if (timer === null) {{
                start();
            }} else {{
                stop();
            }}
        }});

        nextButton.addEventListener("click", () => {{
            if (timer === null) {{
                advanceFrame();
            }}
        }});

        resetButton.addEventListener("click", () => {{
            stop();
            changes = 0;
            showFrame(0);
            start();
        }});

        showFrame(0);
        start();
    }})();
    </script>
    """

    display(HTML(html))