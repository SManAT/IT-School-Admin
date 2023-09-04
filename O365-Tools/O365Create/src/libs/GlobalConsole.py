from rich.console import Console
from rich.theme import Theme

""" A Wrapper for Rich Module """
custom_theme = Theme({
    "info": "#ffff00",
    "warning": "#55ff55",
    "error": "#fe5c1f",
    "default": "#c0c0c0"
})

console = Console(highlight=False, theme=custom_theme)
