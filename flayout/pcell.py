# AUTOGENERATED! DO NOT EDIT! File to edit: source/03_pcell.ipynb (unless otherwise specified).

__all__ = ['pcell']

# Cell
from typing import Callable
from inspect import Parameter, Signature, signature
import pya

# Internal Cell
def _klayout_type(param: Parameter):
    type_map = {
        pya.PCellDeclarationHelper.TypeInt: pya.PCellDeclarationHelper.TypeInt,
        "TypeInt": pya.PCellDeclarationHelper.TypeInt,
        "int": pya.PCellDeclarationHelper.TypeInt,
        int: pya.PCellDeclarationHelper.TypeInt,
        pya.PCellDeclarationHelper.TypeDouble: pya.PCellDeclarationHelper.TypeDouble,
        "TypeDouble": pya.PCellDeclarationHelper.TypeDouble,
        "float": pya.PCellDeclarationHelper.TypeDouble,
        float: pya.PCellDeclarationHelper.TypeDouble,
        pya.PCellDeclarationHelper.TypeString: pya.PCellDeclarationHelper.TypeString,
        "TypeString": pya.PCellDeclarationHelper.TypeString,
        "str": pya.PCellDeclarationHelper.TypeString,
        str: pya.PCellDeclarationHelper.TypeString,
        pya.PCellDeclarationHelper.TypeBoolean: pya.PCellDeclarationHelper.TypeBoolean,
        "TypeBoolean": pya.PCellDeclarationHelper.TypeBoolean,
        "bool": pya.PCellDeclarationHelper.TypeBoolean,
        bool: pya.PCellDeclarationHelper.TypeBoolean,
        pya.PCellDeclarationHelper.TypeLayer: pya.PCellDeclarationHelper.TypeLayer,
        "TypeLayer": pya.PCellDeclarationHelper.TypeLayer,
        "LayerInfo": pya.PCellDeclarationHelper.TypeLayer,
        pya.LayerInfo: pya.PCellDeclarationHelper.TypeLayer,
        pya.PCellDeclarationHelper.TypeShape: pya.PCellDeclarationHelper.TypeShape,
        "TypeShape": pya.PCellDeclarationHelper.TypeShape,
        "Shape": pya.PCellDeclarationHelper.TypeShape,
        pya.Shape: pya.PCellDeclarationHelper.TypeShape,
        pya.PCellDeclarationHelper.TypeList: pya.PCellDeclarationHelper.TypeList,
        "TypeList": pya.PCellDeclarationHelper.TypeList,
        "list": pya.PCellDeclarationHelper.TypeList,
        list: pya.PCellDeclarationHelper.TypeList,
    }
    annotation = param.annotation
    if annotation is Parameter.empty:
        annotation = type(param.default)
    if not annotation in type_map:
        raise ValueError(
            f"Cannot create pcell. Parameter {param.name!r} has unsupported type: {annotation!r}"
        )
    return type_map[annotation]

# Internal Cell
def _python_type(param: Parameter):
    type_map = {
        pya.PCellDeclarationHelper.TypeInt: int,
        "TypeInt": int,
        "int": int,
        int: int,
        pya.PCellDeclarationHelper.TypeDouble: float,
        "TypeDouble": float,
        "float": float,
        float: float,
        pya.PCellDeclarationHelper.TypeString: str,
        "TypeString": str,
        "str": str,
        str: str,
        pya.PCellDeclarationHelper.TypeBoolean: bool,
        "TypeBoolean": bool,
        "bool": bool,
        bool: bool,
        pya.PCellDeclarationHelper.TypeLayer: pya.LayerInfo,
        "TypeLayer": pya.LayerInfo,
        "LayerInfo": pya.LayerInfo,
        pya.LayerInfo: pya.LayerInfo,
        pya.PCellDeclarationHelper.TypeShape: pya.Shape,
        "TypeShape": pya.Shape,
        "Shape": pya.Shape,
        pya.Shape: pya.Shape,
        pya.PCellDeclarationHelper.TypeList: list,
        "TypeList": list,
        "list": list,
        list: list,
    }
    annotation = param.annotation
    if annotation is Parameter.empty:
        annotation = type(param.default)
    if not annotation in type_map:
        raise ValueError(
            f"Cannot create pcell. Parameter {param.name!r} has unsupported type: {annotation!r}"
        )
    return type_map[annotation]

# Internal Cell
def _pcell_parameters(func: Callable):
    sig = signature(func)
    params = sig.parameters

    new_params = {
        "name": Parameter(
            "name", kind=Parameter.KEYWORD_ONLY, default=func.__name__, annotation=str
        )
    }

    for name, param in params.items():
        if param.kind == Parameter.VAR_POSITIONAL:
            raise ValueError(
                f"Cannot create pcell from functions with var positional [*args] arguments."
            )
        elif param.kind == Parameter.VAR_KEYWORD:
            raise ValueError(
                f"Cannot create pcell from functions with var keyword [**kwargs] arguments."
            )
        elif param.kind == Parameter.POSITIONAL_ONLY:
            raise ValueError(
                f"Cannot create pcell from functions with positional arguments. Please use keyword arguments."
            )
        elif (param.kind == Parameter.POSITIONAL_OR_KEYWORD) and (param.default is Parameter.empty):
            raise ValueError(
                f"Cannot create pcell from functions with positional arguments. Please use keyword arguments."
            )
        new_params[name] = Parameter(
            name,
            kind=Parameter.KEYWORD_ONLY,
            default=param.default,
            annotation=_python_type(param),
        )
    return new_params

# Cell

def pcell(func):
    """create a KLayout PCell from a native python function

    Args:
        func: the function creating a KLayout cell

    Returns:
        the Klayout PCell
    """
    params = _pcell_parameters(func)

    def init(self):
        pya.PCellDeclarationHelper.__init__(self)
        for name, param in params.items():
            self.param(
                name,
                _klayout_type(param),
                name.replace("_", " "),
                default=param.default,
            )
        self.func = func
        self.names = tuple(params)

    def call(self, **kwargs):
        name = kwargs.pop("name", func.__name__)
        keys = signature(self.func).parameters
        if name in keys:
            obj = self.func(**kwargs)
        else:
            obj = self.func(**kwargs, name=name)
        obj.name = name
        return obj

    def produce_impl(self):
        kwargs = {name: getattr(self, name) for name in self.names}
        cell = self(**kwargs)
        self.cell.copy_tree(cell)

    def display_text_impl(self):
        return f"{self.name}<{self.__class__.__name__}>"

    DynamicPCell = type(
        func.__name__,
        (pya.PCellDeclarationHelper,),
        {
            "__init__": init,
            "__call__": call,
            "__doc__": func.__doc__
            if func.__doc__ is not None
            else f"a {func.__name__} PCell.",
            "produce_impl": produce_impl,
            "display_text_impl": display_text_impl,
        },
    )
    pcell = DynamicPCell()
    pcell.__signature__ = Signature(list(params.values()), return_annotation=pya.Cell)
    pcell.name = func.__name__
    return pcell