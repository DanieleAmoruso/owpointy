# OWPOINTYS! AN INTERACTIVE OPUNTIA DIAGNOSTIC KEY

#### Video Demo: <https://youtu.be/G9idZwrEkJE>

#### Description:
**Owpointys!** is a command-line botanical identification tool designed to determine species belonging to the cactus genus *Opuntia* (family Cactaceae). Identifying *Opuntia* taxa in field and herbarium settings poses distinct taxonomic challenges due to extensive phenotypic plasticity, interspecific hybridization, and overlapping vegetative morphology.

This program implements an interactive multi-access diagnostic key that prioritizes diagnostic floral and fruit traits over vegetative features, while tolerating intraspecific polymorphism and varying degrees of user uncertainty.

---

### Botanical Logic and Trait Prioritization

Traditional dichotomous keys force the user through rigid, pre-determined decision trees. If a plant is not in flower, the user is frequently unable to proceed. **Owpointys!** resolves this issue through an ordered, multi-access filtering workflow:

1. **Reproductive Features First:** Organ traits such as `flower_color` and `fruit_color` exhibit low phenotypic plasticity and carry the highest diagnostic reliability.
2. **Vegetative Structures Second:** Cladode morphology (`stem_color`, `cladode_shape`), glochids, and spines provide strong corroborative evidence and remain observable year-round.
3. **Habit Last:** General growth habit (`shrub`, `tree`, `prostrate`) is evaluated last because it varies significantly with microclimate, soil depth, and exposure.

---

### Core Components and File Structure

The project consists of three core files:

#### 1. `project.py`
Contains the core analytical pipeline and interactive CLI orchestration:
* **`load_species_data(filepath)`**: Safely reads taxonomic descriptors from a UTF-8 encoded CSV dataset using Python's `csv.DictReader`. Raises an explicit `FileNotFoundError` if the file cannot be located.
* **`parse_numeric_val(text)`**: A helper utility powered by regular expressions (`re`) that extracts integer and floating-point values from strings, stripping away measurement units (such as `cm` or `mm`).
* **`check_trait_match(cell_value, query_value)`**: Evaluates user input against database entries. It supports exact matching, multi-state polymorphic cells delimited by slashes (e.g., `violet/purple`), and continuous numerical range evaluations (e.g., verifying if `15` falls within `10-20 cm`).
* **`filter_taxa(dataset, feature, query_value)`**: Evaluates candidate taxa against user choices. If the user answers `unknown`, no filtering is applied to preserve active candidates.
* **`calculate_confidence(matches_count, answered_steps, total_steps)`**: Generates a deterministic confidence percentage ($0.0\% - 100.0\%$). It rewards comprehensive diagnostic inputs while penalizing unresolved ambiguity if multiple taxa match the final trait set.
* **`get_sorted_features(sample_row)`**: Inspects dataset headers dynamically, excludes non-diagnostic metadata (such as species names and width metrics), and orders the remaining columns according to the defined botanical hierarchy.
* **`main()`**: Displays the ASCII cladode banner, guides the user through the diagnostic sequence, validates input choices, and generates a structured Diagnostic Report.

#### 2. `test_project.py`
Implements thorough unit tests using `pytest` to guarantee deterministic software behavior:
* `test_load_species_data()` verifies correct dataset parsing and exception handling.
* `test_filter_taxa()` tests exact string matches, slash-delimited trait resolution, `unknown` flag preservation, out-of-bounds inputs, and numerical range matches with attached units.
* `test_calculate_confidence()` tests zero-matches, edge-case divisions, full completeness (100%), partial completeness, and ambiguity penalties.

#### 3. `opuntia_data.csv`
A curated morphological matrix of *Opuntia* taxa, including diagnostic fields for flower color, fruit color, stem color, spine presence, spine color, glochid color, habit, and cladode dimensions.

---

### Execution and Installation

To execute the interactive diagnostic key:
```bash
python project.py
