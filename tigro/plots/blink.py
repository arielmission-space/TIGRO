import time
import matplotlib.pyplot as plt

from IPython.display import display


def blink(image1, image2, interval=0.5, n_cycles=20, **imshow_kwargs):
    """
    Alternately display two images in a Jupyter notebook.

    The function creates a single Matplotlib figure and repeatedly updates it
    to show ``image1`` and ``image2`` in sequence. Each image remains visible
    for ``interval`` seconds, and the alternation is repeated for
    ``n_cycles`` cycles.

    Parameters
    ----------
    image1 : array-like
        First image to display. It must have a shape accepted by
        :func:`matplotlib.pyplot.imshow`.

    image2 : array-like
        Second image to display. It should normally have the same shape as
        ``image1``.

    interval : float, optional
        Time, in seconds, for which each image is displayed. The default is
        0.5 seconds.

    n_cycles : int, optional
        Number of complete image1-image2 alternation cycles. The default is
        20.

    **imshow_kwargs
        Additional keyword arguments passed to
        :meth:`matplotlib.axes.Axes.imshow`, such as ``cmap``, ``vmin``,
        ``vmax``, ``origin``, or ``interpolation``.

    Returns
    -------
    None
        The function updates the displayed figure in place and does not return
        a value.

    Notes
    -----
    This function is intended for use in a Jupyter or IPython notebook, where
    ``IPython.display.display`` supports updating an existing display.

    The total nominal display time is approximately::

        2 * interval * n_cycles

    Examples
    --------
    Blink between two grayscale images using the same intensity scale:

    >>> blink(image1, image2, interval=0.25, n_cycles=10,
    ...       cmap="gray", vmin=0, vmax=1)
    """
    fig, ax = plt.subplots(figsize=(8, 8))

    artist = ax.imshow(image1, **imshow_kwargs)
    title = ax.set_title("Image 1")
    ax.axis("off")

    handle = display(fig, display_id=True)
    plt.close(fig)

    for _ in range(n_cycles):
        artist.set_data(image1)
        title.set_text("Image 1")
        handle.update(fig)
        time.sleep(interval)

        artist.set_data(image2)
        title.set_text("Image 2")
        handle.update(fig)
        time.sleep(interval)