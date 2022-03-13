# AUTOGENERATED! DO NOT EDIT! File to edit: source/04_io.ipynb (unless otherwise specified).

__all__ = ['read_gds', 'save_gds']

# Internal Cell
import os

import pya

# Cell
def read_gds(fp: str) -> pya.Layout:
    """load a layout

    Args:
        fp: the path to the layout to load

    Returns:
        the loaded layout
    """
    if isinstance(fp, str):
        fp = os.path.abspath(os.path.expanduser(fp))
    layout = pya.Layout()
    layout.read(fp)
    return layout

# Cell
def save_gds(layout: pya.Layout, fp: str):
    """save a layout

    Args:
        layout: the layout to save
        fp: the path where to save the layout
    """
    if isinstance(fp, str):
        fp = os.path.abspath(os.path.expanduser(fp))
    if isinstance(layout, pya.Layout):
        layout.write(fp)
    else:
        raise ValueError(f"Don't know how to save type {layout.__class__.__name__}.")