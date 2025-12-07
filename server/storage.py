import base64
import json
import os
import time
import uuid
from pathlib import Path

# Support both module import and direct execution
try:
    from .utils import ensure_dir
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from utils import ensure_dir


class Storage:
    """Manages resident data and file storage."""

    def __init__(self, base_path):
        self.base = Path(base_path)
        ensure_dir(self.base)
        self.residents_file = self.base / 'residents.json'
        self._ensure_files()
        self._master_key = 'super-secret-demo-key'

    def _ensure_files(self):
        """Ensure residents.json exists."""
        if not self.residents_file.exists():
            with open(self.residents_file, 'w') as f:
                json.dump([], f)

    def master_key(self):
        return self._master_key

    def list_residents(self):
        """List all residents."""
        with open(self.residents_file) as f:
            return json.load(f)

    def create_resident(self, name, room, **kwargs):
        """Create a new resident with additional fields."""
        res = {
            'id': str(uuid.uuid4()),
            'name': name,
            'room': room,
            'created': time.time()
        }
        # Add any additional fields
        for key, value in kwargs.items():
            if value:  # Only add non-empty values
                res[key] = value
        
        lst = self.list_residents()
        lst.append(res)
        with open(self.residents_file, 'w') as f:
            json.dump(lst, f, indent=2)
        d = self.base / res['id']
        ensure_dir(d)
        return res

    def get_resident(self, rid):
        """Get resident by ID."""
        for r in self.list_residents():
            if r['id'] == rid:
                return r
        return None

    def update_resident(self, rid, obj):
        """Update resident data."""
        lst = self.list_residents()
        for i, r in enumerate(lst):
            if r['id'] == rid:
                lst[i] = obj
                with open(self.residents_file, 'w') as f:
                    json.dump(lst, f, indent=2)
                return obj
        return None

    def save_resident_photo(self, rid, fileobj):
        """Save resident photo."""
        d = self.base / rid
        ensure_dir(d)
        path = d / 'photo.jpg'
        fileobj.save(str(path))
        return str(path)

    def save_resident_voice(self, rid, fileobj):
        """Save resident voice sample."""
        d = self.base / rid
        ensure_dir(d)
        path = d / 'voice.wav'
        fileobj.save(str(path))
        return str(path)

    def save_temp_b64(self, name, b64str):
        """Save temporary file from base64 string."""
        data = base64.b64decode(b64str)
        p = self.base / name
        with open(p, 'wb') as f:
            f.write(data)
        return str(p)
