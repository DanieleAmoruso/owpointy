import csv
import re
import sys

ASCII_BANNER = r"""
          \________/                                \________/
          \/ : : : :\/                           _\ \/ : : : :\/
          | : : : : :|/                          <O=| : : : : :|
   \______\_________/-         owpointys!         / -\________/__/
   / : : : \            ---------------------            / : : : \
 \| : : : : |/          An Interactive Opuntia         \| : : : : |/
 - \_______/___/           Diagnostic Key              \_\_______/ -
        /: : : :\/  /_                             _\  \/: : : :\
       |  : : :  |=|O >                           < O|=|  : : :  |
        \_______/   \                               /   \_______/
"""

BOTANICAL_HIERARCHY = [
    "flower",
    "fruit",
    "cladode",
    "stem",
    "spine",
    "glochid",
    "areole",
    "habit",
]


def parse_numeric_val(text):
    match = re.search(r"[-+]?\d*\.?\d+", text)
    return float(match.group()) if match else None


def check_trait_match(cell_value, query_value):
    clean_cell = cell_value.strip().lower()
    clean_query = query_value.strip().lower()

    if clean_cell == clean_query:
        return True

    options = [opt.strip() for opt in clean_cell.split("/")]
    if clean_query in options:
        return True

    query_num = parse_numeric_val(clean_query)
    if query_num is not None:
        range_match = re.search(r"(\d*\.?\d+)\s*-\s*(\d*\.?\d+)", clean_cell)
        if range_match:
            low = float(range_match.group(1))
            high = float(range_match.group(2))
            if low <= query_num <= high:
                return True
        else:
            single_num = parse_numeric_val(clean_cell)
            if single_num is not None and single_num == query_num:
                return True

    return False


def load_species_data(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")


def filter_taxa(dataset, feature, query_value):
    if query_value.lower() == "unknown":
        return dataset

    filtered = []
    for item in dataset:
        raw_val = item.get(feature, "")
        if check_trait_match(raw_val, query_value):
            filtered.append(item)

    return filtered


def calculate_confidence(matches_count, answered_steps, total_steps):
    if matches_count <= 0 or total_steps <= 0:
        return 0.0

    base_score = (answered_steps / total_steps) * 100

    if matches_count == 1:
        return round(base_score, 2)
    else:
        penalty = 1 / matches_count
        return round(base_score * penalty, 2)


def get_sorted_features(sample_row):
    excluded_fields = {
        "species",
        "taxon",
        "scientific_name",
        "id",
        "width",
        "cladode_width",
        "stem_width",
    }
    available_fields = [
        k
        for k in sample_row.keys()
        if k.lower() not in excluded_fields and "width" not in k.lower()
    ]

    def ranking(field_name):
        lower_name = field_name.lower()
        for idx, key in enumerate(BOTANICAL_HIERARCHY):
            if key in lower_name:
                return idx
        return len(BOTANICAL_HIERARCHY)

    return sorted(available_fields, key=ranking)


def main():
    print(ASCII_BANNER)

    try:
        full_dataset = load_species_data("opuntia_data.csv")
    except FileNotFoundError as e:
        sys.exit(f"Error: {e}")

    if not full_dataset:
        sys.exit("Error: Dataset is empty.")

    features = get_sorted_features(full_dataset[0])
    candidates = list(full_dataset)
    total_steps = len(features)
    answered_steps = 0

    print("\n--- Interactive Botanical Identification Key ---")
    print("Type your answer from the options, or 'unknown' to skip.\n")

    for feature in features:
        options = set()
        for item in full_dataset:
            raw_val = item.get(feature, "")
            if raw_val:
                for val in raw_val.split("/"):
                    clean_val = val.strip().lower()
                    if clean_val:
                        options.add(clean_val)

        options_display = "/".join(sorted(options)) + "/unknown"

        while True:
            prompt_label = feature.replace("_", " ").capitalize()
            user_input = (
                input(f"{prompt_label} [{options_display}]: ").strip().lower()
            )

            is_valid = user_input == "unknown" or user_input in options
            if not is_valid and parse_numeric_val(user_input) is not None:
                for opt in options:
                    if check_trait_match(opt, user_input):
                        is_valid = True
                        break

            if is_valid:
                break
            print("Invalid input. Please choose from the displayed options.")

        if user_input != "unknown":
            answered_steps += 1

        candidates = filter_taxa(candidates, feature, user_input)

    confidence = calculate_confidence(
        len(candidates), answered_steps, total_steps
    )

    print("\n================ DIAGNOSTIC REPORT ================")
    print(f"Confidence score: {confidence}%\n")

    if len(candidates) == 1:
        match = candidates[0]
        taxon_name = match.get("species") or match.get("taxon") or "Unknown"
        print(f"Identified Taxon: {taxon_name}")
        print("-" * 50)
        for key, value in match.items():
            if (
                key.lower() not in {"species", "taxon"}
                and "width" not in key.lower()
                and value
            ):
                clean_key = key.replace("_", " ").capitalize()
                print(f"  {clean_key:<25}: {value}")
    elif len(candidates) > 1:
        print(f"Ambiguous diagnosis: {len(candidates)} species match:")
        for sp in candidates:
            taxon_name = sp.get("species") or sp.get("taxon") or "Unknown"
            print(f" - {taxon_name}")
    else:
        print("No matching species found for the selected traits.")

    print("===================================================\n")


if __name__ == "__main__":
    main()
