import json
from pathlib import Path


class Repository:
    def __init__(self, path = "."):
        self.path = Path(path).resolve()
        self.ditto_dir = self.path / ".ditto"

        #Objects
        self.objects_dir = self.ditto_dir / "objects"

        #Refs
        self.ref_dir = self.ditto_dir / "refs"
        self.heads_dir = self.ref_dir / "heads"

        #HEAD
        self.head_file = self.ditto_dir / "HEAD"

        #Index
        self.index_file = self.ditto_dir / "index"

    def init(self) -> bool:
        if self.ditto_dir.exists():
            return False
        
        # Creating Directories:
        self.ditto_dir.mkdir()
        self.objects_dir.mkdir()
        self.ref_dir.mkdir()
        self.heads_dir.mkdir()

        # Initial HEAD
        self.head_file.write_text("Ref: refs/heads/master\n")

        self.index_file.write_text(json.dumps({}, indent=2))

        print(f"Initialized empty Ditto repository in {self.ditto_dir}")

        return True