from pathlib import Path

from easygram.integrations.tdlib.gateway import TdlibGateway


def test_candidate_library_paths_include_common_tdjson_locations(tmp_path: Path) -> None:
    gateway = TdlibGateway(tdlib_root=tmp_path)

    candidates = gateway.candidate_library_paths()

    assert tmp_path / "tdjson.dll" in candidates
    assert tmp_path / "bin" / "tdjson.dll" in candidates
    assert tmp_path / "lib" / "libtdjson.dll" in candidates


def test_load_library_reports_missing_tdjson(tmp_path: Path) -> None:
    gateway = TdlibGateway(tdlib_root=tmp_path)

    loaded = gateway.load_library()

    assert loaded is False
    assert gateway.last_error
