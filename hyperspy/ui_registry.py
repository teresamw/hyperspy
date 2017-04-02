'''Registry of user interface widgets.

Format {"tool_key" : {"toolkit" : <function(obj, display, **kwargs)>}}

The ``tool_key` is defined by the "model function" to which the widget provides
and user interface. That function gets the widget function from this registry
and executes it passing the ``obj``, ``display`` and any extra keyword
arguments. When ``display`` is true, ``function`` displays the widget. If
``False`` it returns a dictionary with whatever is needed to display the
widgets externally (usually for testing or customisation purposes).

'''

import functools
import types

from hyperspy.misc.utils import isiterable

UI_REGISTRY = {}

toolkit_registry = set()


def register_widget(toolkit, toolkey):
    """Decorator to register a UI widget.

    Parameters
    ----------
    f: function
        Function that returns or display the UI widget. The signature must
        include ``obj``, ``display`` and ``**kwargs``.
    toolkit: string
        The name of the widget toolkit e.g. ipywidgets
    toolkey: string
        The "key" of the tool for which the widget provides an interface. If
        the toolkey is not in the ``UI_REGISTRY`` dictionary a ``NameError``
        is raised.

    Returns
    -------
    widgets: dictionary or None
        Dictionary containing the widget objects if display is False, else None.

    """
    if not toolkey in UI_REGISTRY:
        raise NameError("%s is not a registered toolkey" % toolkey)
    toolkit_registry.add(toolkit)

    def decorator(f):
        UI_REGISTRY[toolkey][toolkit] = f
        return f
    return decorator


def register_toolkey(toolkey):
    """Register a toolkey.

    Parameters
    ----------
    toolkey: string

    """
    if toolkey in UI_REGISTRY:
        raise NameError(
            "Another tool has been registered with the same name.")
    UI_REGISTRY[toolkey] = {}


def get_gui(self, toolkey, display=True, toolkit=None, **kwargs):
    error = "There is no user interface registered for this feature."
    from hyperspy.ui_registry import UI_REGISTRY
    toolkits = None
    if isinstance(toolkit, str):
        toolkits = (toolkit,)
    elif isiterable(toolkit):
        toolkits = toolkit
    elif toolkit is not None:
        raise ValueError(
            "`toolkit` must be a string, an iterable of strings or None.")
    if toolkey not in UI_REGISTRY or not UI_REGISTRY[toolkey]:
        raise NotImplementedError(error)
    if not display:
        widgets = {}
    for toolkit, f in UI_REGISTRY[toolkey].items():
        if toolkits is None or toolkit in toolkits:
            thisw = f(obj=self, display=display, **kwargs)
            if not display:
                widgets[toolkit] = thisw
    if not display:
        return widgets


def get_partial_gui(toolkey):
    def pg(self, display=True, toolkit=None, **kwargs):
        return get_gui(self, toolkey=toolkey, display=display,
                       toolkit=None, **kwargs)
    return pg

GUI_DT = """Display or return interactive GUI element if available.

Parameters
----------
display: bool
    If True, display the user interface widgets. If False, return the widgets
    container in a dictionary, usually for customisation or testing.
toolkit: str, iterable of strings or None
    If None (default), all available widgets are displayed or returned. If
    string, only the widgets of the selected toolkit are displayed if available.
    If an interable of toolkit strings, the widgets of all listed toolkits are
    displayed or returned.

"""


def add_gui_method(toolkey):
    def decorator(cls):
        register_toolkey(toolkey)
        # Not using functools.partialmethod because it is not possible to set
        # the docstring that way.
        setattr(cls, "gui", get_partial_gui(toolkey))
        setattr(cls.gui, "__doc__", GUI_DT)
        return cls
    return decorator


register_toolkey("interactive_range_selector")
register_toolkey("navigation_sliders")
register_toolkey("Signal1D.spikes_removal_tool")
register_toolkey("Signal1D.calibrate")
register_toolkey("Signal1D.smooth_savitzky_golay")
register_toolkey("Signal1D.smooth_lowess")
register_toolkey("Signal1D.smooth_total_variation")
register_toolkey("Signal1D.remove_background")
register_toolkey("Signal1D.integrate_in_range")
register_toolkey("Model1D.fit_component")
register_toolkey("load")
