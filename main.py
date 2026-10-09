import argparse
import sys
from repository import Repository


def main ():
    parser = argparse.ArgumentParser(description="Let's make a git clone")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")


    init_parser = subparsers.add_parser("init", help="Initializing a new reposity")
    add_parser = subparsers.add_parser("add", help="Adding files and folders")

    add_parser.add_argument("paths", nargs='+', help="Add file contents to ditto")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    repo = Repository()
    
    try:
        if args.command == "init":
            if not repo.init():
                print("Repository already exists")
                return
        elif args.command =="add":
            if not repo.ditto_dir.exists():
                print("Not a ditto repository")
                return
            for path in args.paths:
                repo.add_path(path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

main()