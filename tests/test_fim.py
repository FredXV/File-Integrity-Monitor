import fim
import hashlib

# ---------- hash_file ----------


def test_hash_file_known_value(tmp_path):

    f = tmp_path / "hello.txt"
    f.write_bytes(b"hello")


    assert fim.hash_file(f) == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"


def test_hash_file_empty_file(tmp_path):

    f = tmp_path / "empty.txt"
    f.write_bytes(b"")

    assert fim.hash_file(f) == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def test_hash_file_same_content_same_hash(tmp_path):

    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_bytes(b"same content")
    b.write_bytes(b"same content")

    assert fim.hash_file(a) == fim.hash_file(b)


def test_hash_file_different_content_different_hash(tmp_path):

    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_bytes(b"hello")
    b.write_bytes(b"hellp")

    assert fim.hash_file(a) != fim.hash_file(b)


def test_hash_file_larger_than_one_chunk(tmp_path):

    data = b"a" * 20000

    f = tmp_path / "big.bin"
    f.write_bytes(data)

    assert fim.hash_file(f) == hashlib.sha256(data).hexdigest()


# ---------- compare ----------


def test_compare_unchanged_file():

    baseline = {"hello.txt": "abc123"}
    current = {"hello.txt": "abc123"}

    result = fim.compare(baseline, current)

    assert result["modified"] == []
    assert result["added"] == []
    assert result["deleted"] == []


def test_compare_detects_all_changes():

    baseline = {

        "stable.txt": "hash111",
        "changed.txt": "hash222",
        "missing.txt": "hash333"
    }

    current = {

        "stable.txt": "hash111",
        "changed.txt": "hash999",
        "brand_new.txt": "hash444"
    }

    result = fim.compare(baseline, current)

    assert result["modified"] == ["changed.txt"]
    assert result["added"] == ["brand_new.txt"]
    assert result["deleted"] == ["missing.txt"]


def test_compare_empty_baseline_marks_everything_added():

    current = {"a.txt": "111", "b.txt": "222"}

    result = fim.compare({}, current)

    assert result["added"] == ["a.txt", "b.txt"]
    assert result["modified"] == []
    assert result["deleted"] == []


# ---------- scan_folder ----------


def test_scan_folder_indexes_directory(tmp_path):

    mock_monitored_dir = tmp_path / "Monitored_files"
    mock_monitored_dir.mkdir()

    sample_file = mock_monitored_dir / "sample.txt"
    sample_file.write_bytes(b"test data content")


    hashes, skipped = fim.scan_folder(mock_monitored_dir)

    assert hashes["sample.txt"] == fim.hash_file(sample_file)
    assert skipped == []


def test_scan_folder_includes_subfolders(tmp_path):

    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "notes.txt").write_bytes(b"nested")
    (tmp_path / "top.txt").write_bytes(b"top")

    hashes, skipped = fim.scan_folder(tmp_path)

    assert set(hashes) == {"top.txt", "sub/notes.txt"}
    assert skipped == []


def test_scan_folder_empty_folder(tmp_path):

    hashes, skipped = fim.scan_folder(tmp_path)

    assert hashes == {}
    assert skipped == []