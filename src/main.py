from cli.terminal import launch_cli
from scripts.init_db import init_db

def main():
    init_db()
    launch_cli()


if __name__ == "__main__":
    main()