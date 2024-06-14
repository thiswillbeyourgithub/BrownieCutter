import fire

from .BrownieCutter import BrownieCutter

def cli_launcher() -> None:
    fire.Fire(BrownieCutter)

if __name__ == "__main__":
    cli_launcher()