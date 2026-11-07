from pathlib import Path
import hashlib, sqlite3

SCHEMA = """CREATE TABLE IF NOT EXISTS files (path TEXT PRIMARY KEY, size INTEGER NOT NULL, mtime_ns INTEGER NOT NULL, sha256 TEXT NOT NULL, indexed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"""

class FileInventory:
    """Reference-only local inventory; it never moves, deletes or modifies source files."""
    def __init__(self, database):
        self.database = Path(database); self.database.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.database) as db: db.execute(SCHEMA)

    def update(self, paths):
        rows=[]
        for value in paths:
            path=Path(value).resolve()
            stat=path.stat(); digest=hashlib.sha256()
            with path.open('rb') as stream:
                for block in iter(lambda: stream.read(1024*1024), b''): digest.update(block)
            rows.append((str(path), stat.st_size, stat.st_mtime_ns, digest.hexdigest()))
        with sqlite3.connect(self.database) as db:
            db.executemany('INSERT INTO files(path,size,mtime_ns,sha256) VALUES(?,?,?,?) ON CONFLICT(path) DO UPDATE SET size=excluded.size,mtime_ns=excluded.mtime_ns,sha256=excluded.sha256,indexed_at=CURRENT_TIMESTAMP', rows)
        return len(rows)

    def list(self):
        with sqlite3.connect(self.database) as db: return db.execute('SELECT path,size,mtime_ns,sha256,indexed_at FROM files ORDER BY path').fetchall()

    def remove(self, path):
        with sqlite3.connect(self.database) as db: db.execute('DELETE FROM files WHERE path=?', (str(Path(path).resolve()),))

    def missing(self):
        return [row for row in self.list() if not Path(row[0]).exists()]
