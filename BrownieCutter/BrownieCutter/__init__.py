import fire

from .BrownieCutter import BrownieCutter

def cli_launcher() -> None:
    fire.Fire(BrownieCutter().create)

if __name__ == "__main__":
    cli_launcher()
