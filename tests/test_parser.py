from schconv import parser


def test_extract_sheet_title_prefers_descriptive_line():
    lines = [
        "Engineer",
        "Title",
        "USB HOST, MIC, Audio Out",
        "Audio Jack",
        "GND",
    ]
    assert parser._extract_sheet_title(lines) == "USB HOST, MIC, Audio Out"


def test_extract_sheet_title_returns_none_when_no_match():
    lines = ["ENGINEER", "GND", "VCC3V3", "R1", "R2"]
    assert parser._extract_sheet_title(lines) is None


def test_top_terms_filters_stop_words():
    lines = [
        "Power Regulation",
        "Power Select",
        "Input Voltage 7-15V",
        "Power Regulation",
    ]
    assert parser._top_terms(lines, limit=3) == ["power", "regulation", "select"]
