from rich.console import Console
from rich.theme import Theme


class MyConsole():
  """ A Wrapper for Rich Module """
  custom_theme = Theme({
      "info": "#ffff00",
      "warning": "#55ff55",
      "error": "#fe5c1f",
      "default": "#c0c0c0"
  })

  def __init__(self):
    self.console = Console(highlight=False, theme=self.custom_theme)

  def error(self, msg):
    self.console.print("[error]%s[/]" % msg)

  def warning(self, msg):
    self.console.print("[warning]%s[/]" % msg)

  def info(self, msg):
    self.console.print("[info]%s[/]" % msg)

  def print(self, msg):
    self.console.print("[default]%s[/]" % msg)
