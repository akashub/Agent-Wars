from agentwars.store import Store, sha256_bundle


def test_hash_is_order_independent_and_stable():
    a = sha256_bundle([("t.json", b"{}"), ("d.diff", b"x")])
    b = sha256_bundle([("d.diff", b"x"), ("t.json", b"{}")])
    assert a == b and len(a) == 64


def test_record_and_recompute_detects_tamper(tmp_path):
    store = Store(tmp_path)
    store.init_db()
    h = store.put_transcript("run1", b'{"steps": []}')
    store.record_run(
        run_id="run1",
        war_id="w1",
        agent_version="a@1",
        seed=7,
        tokens_used=10,
        content_hash=h,
        transcript_ref="run1.json",
    )
    assert store.get_run("run1")["content_hash"] == h
    assert store.recompute_hash("run1") == h
    (tmp_path / "transcripts" / "run1.json").write_bytes(b"TAMPERED")
    assert store.recompute_hash("run1") != h
