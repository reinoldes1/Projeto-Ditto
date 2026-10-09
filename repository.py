import hashlib
import json
from pathlib import Path
from typing import Dict
import zlib


class DittoObject:
    def __init__(self, obj_type: str, content: bytes):
        self.type = obj_type
        self.content = content
    
    def hash(self) -> str:
        header = f"{self.type} {len(self.content)}\0".encode()
        return hashlib.sha1(header + self.content).hexdigest()
    
    def serialize(self) -> bytes:
        header = f"{self.type} {len(self.content)}\0".encode()
        return zlib.compress(header + self.content)
    
    @classmethod
    def deserialize(cls, data: bytes) -> "DittoObject":
        decompressed = zlib.decompress(data)
        null_index = decompressed.find(b"\0")
        header = decompressed[:null_index]
        content = decompressed[null_index + 1:]

        obj_type, _ = header.split(" ")

        return cls(obj_type, content)

class Blob(DittoObject):
    def __init__(self, content: bytes):
        super().__init__("blob", content)
    
    def get_content(self) -> bytes:
        return self.content

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
        
        self.ditto_dir.mkdir()
        self.objects_dir.mkdir()
        self.ref_dir.mkdir()
        self.heads_dir.mkdir()

        self.head_file.write_text("Ref: refs/heads/master\n")

        self.save_index({})

        print(f"Initialized empty Ditto repository in {self.ditto_dir}")

        return True
    
    def load_index(self) -> Dict[str, str]:
        if not self.index_file.exists():
            return {}
        try:
            return json.loads(self.index_file.read_text())
        except:
            return {}
    
    def store_object(self, obj: DittoObject) -> str:
        obj_hash = obj.hash()
        obj_dir = self.objects_dir / obj_hash[:2]
        obj_file = obj_dir / obj_hash[2:]

        if not obj_file.exists():
            obj_dir.mkdir(exist_ok = True)
            obj_file.write_bytes(obj.serialize())
            
        return obj_hash
    
    def save_index(self, index: Dict[str, str]):
        self.index_file.write_text(json.dumps(index, indent=2))

    def add_file(self, path: str):
        full_path = self.path / path
        if not full_path.exists():
            raise ValueError(f"{path} is neither a file nor a directory")
        
        content = full_path.read_bytes()

        blob = Blob(content)

        blob_hash = self.store_object(blob)

        index = self.load_index()
        index[path] = blob_hash
        
        self.save_index(index)     

        print(f"Added {path}")

    def add_directory(self):
        pass 
    
    def add_path(self, path: str) -> None:
        full_path = self.path / path

        if not full_path.exists():
            raise FileNotFoundError(f"Path {path} not found")
        if full_path.is_file():
            self.add_file(path)
        elif full_path.is_dir():
            self.add_directory(path)
        else:
            raise ValueError(f"{path} is neither a file nor a directory")