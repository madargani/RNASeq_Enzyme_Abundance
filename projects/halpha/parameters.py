import os
import sys
from pathlib import Path

from parameters import Parameters

project_root = str(Path(__file__).resolve().parent.parent.parent)
sys.path.append(project_root)
runtime_root = os.getcwd()


class HalphaParameters(Parameters):
    def __init__(self, verbose=True):
        self.project = "halpha"
        self.value_column = "value"
        self.project_species = ["Athaliana"]
        self.group_columns = ["condition"]
        self.rnaSeq_id_col = "Gene_ID"
        self.error = False
        self.control_id = "6mM"
        self.control_name = "6mM"
        self.trmt_colmn = "condition"
        self.reaction_score_method = "sum"
        self.ignore_organellar_roles = os.path.join(
            project_root, "data", "organellar-encoded_subunits_to_ignore.txt"
        )

        # Baseline Directory Structuring
        self.json_files_folder = os.path.join(
            project_root, "projects", self.project, "inputs"
        )
        self.RNASeq_folder = os.path.join(
            project_root, "projects", self.project, "rnaseq-data"
        )
        self.results_folder = os.environ.get(
            "RESULTS_FOLDER",
            os.path.join(project_root, "projects", self.project, "integration_results"),
        )
        self.reaction_file_suffix = "_reaction_scores.tsv"

        # Initial Directory Existence Testing
        for folder_name, folder_path in [
            ("Models Input", self.json_files_folder),
            ("RNASeq Data", self.RNASeq_folder),
            ("Results Output", self.results_folder),
        ]:
            if not os.path.exists(folder_path):
                print(
                    f"[!] WARNING: {folder_name} folder not found. Expected location: {folder_path}"
                )
                if folder_name == "Results Output":
                    os.makedirs(folder_path, exist_ok=True)
                    print(f"    -> Automatically initialized folder path.")
                else:
                    self.error = True

        # Automated File Discovery & Integrity Mapping
        self.model_paths = {}
        self.rnaseq_paths = {}
        self.rxn_scores_paths = {}  # Added to house optional results files

        if not self.error:
            self._discover_json_models(verbose)
            self._discover_rnaseq_files(verbose)
            self._discover_existing_results(verbose)
            self._validate_discovered_assets()
