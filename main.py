import argparse
import sys
from repository import Repository


def main ():
    parser = argparse.ArgumentParser(description="Let's make a git clone")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")


    init_parsers = subparsers.add_parser("init", help="Initializing a new reposity")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "init":
            repo = Repository()
            if not repo.init():
                print("Repository already exists")
                return
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

main ()