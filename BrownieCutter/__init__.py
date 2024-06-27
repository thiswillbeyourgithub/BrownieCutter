import fire

from .BrownieCutter import BrownieCutter

__all__ = ["BrownieCutter"]

__VERSION__ = BrownieCutter.VERSION

def cli_launcher() -> None:
    fire.Fire(BrownieCutter().create)

if __name__ == "__main__":
    cli_launcher()
