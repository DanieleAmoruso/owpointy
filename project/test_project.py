import pytest
from project import calculate_confidence, filter_taxa, load_species_data

MOCK_DATA = [
    {
        "species": "Opuntia ficus-indica",
        "stem_color": "green",
        "habit": "shrub/tree",
        "cladode_length": "20-50 cm",
    },
    {
        "species": "Opuntia santa-rita",
        "stem_color": "violet/purple",
        "habit": "shrub",
        "cladode_length": "10-20 cm",
    },
    {
        "species": "Opuntia humifusa",
        "stem_color": "dark_green",
        "habit": "prostrate",
        "cladode_length": "5-12 cm",
    },
]


def test_load_species_data():
    data = load_species_data("opuntia_data.csv")
    assert isinstance(data, list)
    assert len(data) > 0
    assert "species" in data[0] or "taxon" in data[0]

    with pytest.raises(FileNotFoundError):
        load_species_data("non_existent_file.csv")


def test_filter_taxa():
    res_exact = filter_taxa(MOCK_DATA, "stem_color", "dark_green")
    assert len(res_exact) == 1
    assert res_exact[0]["species"] == "Opuntia humifusa"

    res_slash = filter_taxa(MOCK_DATA, "stem_color", "purple")
    assert len(res_slash) == 1
    assert res_slash[0]["species"] == "Opuntia santa-rita"

    res_unknown = filter_taxa(MOCK_DATA, "stem_color", "unknown")
    assert len(res_unknown) == 3

    res_none = filter_taxa(MOCK_DATA, "stem_color", "blue")
    assert len(res_none) == 0

    res_range = filter_taxa(MOCK_DATA, "cladode_length", "15")
    assert len(res_range) == 1
    assert res_range[0]["species"] == "Opuntia santa-rita"

    res_unit = filter_taxa(MOCK_DATA, "cladode_length", "10cm")
    assert len(res_unit) == 2
    taxa_matched = {sp["species"] for sp in res_unit}
    assert taxa_matched == {"Opuntia santa-rita", "Opuntia humifusa"}


def test_calculate_confidence():
    assert calculate_confidence(0, 3, 5) == 0.0
    assert calculate_confidence(1, 0, 0) == 0.0
    assert calculate_confidence(1, 5, 5) == 100.0
    assert calculate_confidence(1, 3, 5) == 60.0
    assert calculate_confidence(2, 5, 5) == 50.0
