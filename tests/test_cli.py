import json

from schconv.cli import main


def test_cli_stdout(monkeypatch, capsys):
    monkeypatch.setattr(
        "schconv.cli.parse_pdf",
        lambda _: {"source_file": "x.pdf", "page_count": 1, "pages": [], "global_terms": []},
    )
    rc = main(["fake.pdf"])
    assert rc == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["source_file"] == "x.pdf"


def test_cli_output_file(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "schconv.cli.parse_pdf",
        lambda _: {"source_file": "y.pdf", "page_count": 2, "pages": [], "global_terms": []},
    )
    output = tmp_path / "result.json"
    rc = main(["fake.pdf", "--output", str(output), "--pretty"])
    assert rc == 0
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["page_count"] == 2
