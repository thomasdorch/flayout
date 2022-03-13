# AUTOGENERATED! DO NOT EDIT! File to edit: source/99_example_lib.ipynb (unless otherwise specified).

__all__ = ['rectangle', 'square', 'gf_pcells', 'example_lib']

# Internal Cell
import pya
import flayout as fl

# Cell
@fl.pcell
def rectangle(
    name="rectangle",
    width: float = 1.0,
    height: float = 0.5,
    layer: pya.LayerInfo = pya.LayerInfo(1, 0),
):
    rect = fl.polygon(hull=[(-width/2, -height/2), (width/2, -height/2), (width/2, height/2), (-width/2, height/2)])
    cell = fl.cell(name, shapes={layer: [rect]})
    return cell

# Cell
@fl.pcell
def square(
    name="square",
    width: float = 0.5,
    layer: pya.LayerInfo = pya.LayerInfo(1, 0),
):
    square = fl.polygon(hull=[(-width/2, -width/2), (width/2, -width/2), (width/2, width/2), (-width/2, width/2)])
    cell = fl.cell(name, shapes={layer: [square]})
    return cell

# Cell
gf_pcells = []
try:
    import gdsfactory.components as gfc
except ImportError:
    gfc = None

if gfc is not None:
    gf_pcells += [
        mzi := fl.pcell(gfc.mzi, on_error="ignore"),
        bend_euler := fl.pcell(gfc.bend_euler, on_error="ignore")
    ]

# Cell
example_lib = fl.library(
    "F. E. L.",
    pcells=[rectangle, square, *gf_pcells],
    cells=[],
    description="FLayout Example Library",
)