from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path


def sha256_bundle(items: list[tuple[str, bytes]]) -> str:
    h = hashlib.sha256()
    for name, data in sorted(items, key=lambda x: x[0]):
        h.update(name.encode())
        h.update(b"\0")
        h.update(hashlib.sha256(data).digest())
    return h.hexdigest()


class Store:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.transcripts = self.root / "transcripts"
        self.transcripts.mkdir(parents=True, exist_ok=True)
        self.db_path = self.root / "runs.db"

    def init_db(self) -> None:
        with sqlite3.connect(self.db_path) as c:
            c.execute(
                "CREATE TABLE IF NOT EXISTS runs ("
                "run_id TEXT PRIMARY KEY, war_id TEXT, agent_version TEXT, seed INTEGER,"
                "tokens_used INTEGER, content_hash TEXT, transcript_ref TEXT)"
            )

    def put_transcript(self, run_id: str, payload: bytes) -> str:
        ref = f"{run_id}.json"
        (self.transcripts / ref).write_bytes(payload)
        return sha256_bundle([(ref, payload)])

    def record_run(
        self,
        *,
        run_id,
        war_id,
        agent_version,
        seed,
        tokens_used,
        content_hash,
        transcript_ref,
    ) -> None:
        with sqlite3.connect(self.db_path) as c:
            c.execute(
                "INSERT OR REPLACE INTO runs VALUES (?,?,?,?,?,?,?)",
                (run_id, war_id, agent_version, seed, tokens_used, content_hash, transcript_ref),
            )

    def get_run(self, run_id: str) -> dict:
        with sqlite3.connect(self.db_path) as c:
            c.row_factory = sqlite3.Row
            row = c.execute("SELECT * FROM runs WHERE run_id=?", (run_id,)).fetchone()
        return dict(row) if row else {}

    def recompute_hash(self, run_id: str) -> str:
        run = self.get_run(run_id)
        ref = run["transcript_ref"]
        return sha256_bundle([(ref, (self.transcripts / ref).read_bytes())])
