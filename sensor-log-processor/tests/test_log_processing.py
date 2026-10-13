import json
from pathlib import Path

import pytest

from src.service.log_processing import process_log

class TestDispatch:

    def test_processes_a_log(self, sample_a_path):
        result = process_log(sample_a_path, "A-LOG", write_csv=False)

        assert result["log_type"] == "A-LOG"
        assert result["file_name"] == "SAMPLE-A.LOG"
        assert result["total_records"] > 0

    def test_processes_p_log(self, sample_p_path):
        result = process_log(sample_p_path, "P-LOG", write_csv=False)

        assert result["log_type"] == "P-LOG"
        assert result["file_name"] == "SAMPLE-P.LOG"
        assert result["total_records"] > 0

    def test_rejects_unknown_log_type(self, sample_a_path):
        with pytest.raises(ValueError, match="no soportado"):
            process_log(sample_a_path, "X-LOG", write_csv=False)

    def test_raises_on_missing_file(self, tmp_path):
        missing = tmp_path / "nope.LOG"
        with pytest.raises(FileNotFoundError):
            process_log(str(missing), "A-LOG", write_csv=False)

class TestResponseShape:

    @pytest.mark.parametrize("log_type,fixture_name", [
        ("A-LOG", "sample_a_path"),
        ("P-LOG", "sample_p_path"),
    ])
    def test_required_keys(self, log_type, fixture_name, request):
        path = request.getfixturevalue(fixture_name)
        result = process_log(path, log_type, write_csv=False)

        expected = {
            "log_type", "file_name",
            "total_records", "valid_records", "invalid_records",
            "columns", "records",
        }
        assert expected.issubset(result.keys())

    @pytest.mark.parametrize("log_type,fixture_name", [
        ("A-LOG", "sample_a_path"),
        ("P-LOG", "sample_p_path"),
    ])
    def test_counts_are_consistent(self, log_type, fixture_name, request):
        path = request.getfixturevalue(fixture_name)
        result = process_log(path, log_type, write_csv=False)

        assert result["total_records"] == (
            result["valid_records"] + result["invalid_records"]
        )

    @pytest.mark.parametrize("log_type,fixture_name", [
        ("A-LOG", "sample_a_path"),
        ("P-LOG", "sample_p_path"),
    ])
    def test_records_length_matches_total(self, log_type, fixture_name, request):
        path = request.getfixturevalue(fixture_name)
        result = process_log(path, log_type, write_csv=False)

        assert len(result["records"]) == result["total_records"]

    @pytest.mark.parametrize("log_type,fixture_name", [
        ("A-LOG", "sample_a_path"),
        ("P-LOG", "sample_p_path"),
    ])
    def test_columns_are_unique_strings(self, log_type, fixture_name, request):
        path = request.getfixturevalue(fixture_name)
        result = process_log(path, log_type, write_csv=False)

        assert all(isinstance(c, str) for c in result["columns"])
        assert len(result["columns"]) == len(set(result["columns"]))

MANDATORY_COLUMNS = [
    "source_file",
    "line_number",
    "timestamp",
    "timestamp_utc",
    "is_valid",
]

class TestMandatoryColumns:

    @pytest.mark.parametrize("log_type,fixture_name", [
        ("A-LOG", "sample_a_path"),
        ("P-LOG", "sample_p_path"),
    ])
    def test_all_present(self, log_type, fixture_name, request):
        path = request.getfixturevalue(fixture_name)
        result = process_log(path, log_type, write_csv=False)

        for column in MANDATORY_COLUMNS:
            assert column in result["columns"], f"Falta {column} en {log_type}"

    @pytest.mark.parametrize("log_type,fixture_name", [
        ("A-LOG", "sample_a_path"),
        ("P-LOG", "sample_p_path"),
    ])
    def test_source_file_matches_input_name(self, log_type, fixture_name, request):
        path = request.getfixturevalue(fixture_name)
        result = process_log(path, log_type, write_csv=False)

        for record in result["records"]:
            assert record["source_file"] == result["file_name"]

    @pytest.mark.parametrize("log_type,fixture_name", [
        ("A-LOG", "sample_a_path"),
        ("P-LOG", "sample_p_path"),
    ])
    def test_line_numbers_positive_ints(self, log_type, fixture_name, request):
        path = request.getfixturevalue(fixture_name)
        result = process_log(path, log_type, write_csv=False)

        for record in result["records"]:
            assert isinstance(record["line_number"], int)
            assert record["line_number"] >= 1

    @pytest.mark.parametrize("log_type,fixture_name", [
        ("A-LOG", "sample_a_path"),
        ("P-LOG", "sample_p_path"),
    ])
    def test_is_valid_is_boolean(self, log_type, fixture_name, request):
        path = request.getfixturevalue(fixture_name)
        result = process_log(path, log_type, write_csv=False)

        for record in result["records"]:
            assert isinstance(record["is_valid"], bool)

    @pytest.mark.parametrize("log_type,fixture_name", [
        ("A-LOG", "sample_a_path"),
        ("P-LOG", "sample_p_path"),
    ])
    def test_invalid_records_have_description(self, log_type, fixture_name, request):
        path = request.getfixturevalue(fixture_name)
        result = process_log(path, log_type, write_csv=False)

        for record in result["records"]:
            if not record["is_valid"]:
                desc = (record.get("description_error") or "").strip()
                assert desc, (
                    f"Registro inválido sin description_error en "
                    f"{result['file_name']} línea {record['line_number']}"
                )

class TestCsvWriting:

    def test_writes_csv_by_default(self, sample_a_path, tmp_path):
        out = tmp_path / "out.csv"
        result = process_log(sample_a_path, "A-LOG", output_path=out)

        assert out.exists()
        assert result["output_path"] == str(out)

    def test_does_not_write_when_disabled(self, sample_a_path, tmp_path):
        out = tmp_path / "should_not_exist.csv"
        result = process_log(
            sample_a_path, "A-LOG",
            output_path=out, write_csv=False,
        )

        assert not out.exists()
        assert "output_path" not in result

    def test_default_output_uses_source_stem(self, sample_a_path):
        result = process_log(sample_a_path, "A-LOG")

        expected = Path("data") / "output" / "SAMPLE-A.CSV"
        assert Path(result["output_path"]).name == expected.name
        assert Path(result["output_path"]).exists()

    def test_output_path_creates_parent_dirs(self, sample_a_path, tmp_path):
        out = tmp_path / "nested" / "deep" / "out.csv"
        process_log(sample_a_path, "A-LOG", output_path=out)

        assert out.parent.is_dir()
        assert out.exists()

    def test_written_csv_is_readable(self, sample_a_path, tmp_path):
        import pandas as pd

        out = tmp_path / "out.csv"
        result = process_log(sample_a_path, "A-LOG", output_path=out)

        df = pd.read_csv(out, encoding="utf-8-sig")
        assert len(df) == result["total_records"]
        assert "source_file" in df.columns

class TestJsonSerialization:

    @pytest.mark.parametrize("log_type,fixture_name", [
        ("A-LOG", "sample_a_path"),
        ("P-LOG", "sample_p_path"),
    ])
    def test_result_is_json_serializable(self, log_type, fixture_name, request):
        path = request.getfixturevalue(fixture_name)
        result = process_log(path, log_type, write_csv=False)

        # allow_nan=False revienta si queda algún NaN/Inf
        json.dumps(result, allow_nan=False)