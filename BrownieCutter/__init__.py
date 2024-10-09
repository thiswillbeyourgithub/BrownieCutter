import sys
import fire

from .BrownieCutter import BrownieCutter

__all__ = ["BrownieCutter"]

__VERSION__ = BrownieCutter.VERSION

def cli_launcher() -> None:
    if sys.argv[-1] ==  "--version":
        return(f"BrownieCutter version: {__VERSION__}")
    fire.Fire(BrownieCutter().create)

if __name__ == "__main__":
    cli_launcher()
