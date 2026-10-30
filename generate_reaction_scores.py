#!/usr/bin/env python
import argparse
import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent

module = str(project_root) + "/src/reaction_scores"
if module not in sys.path:
    sys.path.append(module)

# Parameters class
# The parameters dictate where to find the files
# And how to link them to different species/conditions
# Reaction scores
import src.reaction_scores.computeScoresAndPredictions as csp

parser = argparse.ArgumentParser(description="Generate reaction scores")
parser.add_argument(
    "--param-class",
    default="parameters.Parameters",
    help="Dotted path to a Parameters subclass (default: parameters.Parameters)",
)
args = parser.parse_args()

module_name, class_name = args.param_class.rsplit(".", 1)
param_module = __import__(module_name, fromlist=[class_name])
param_class = getattr(param_module, class_name)

project_param = param_class()

for species in project_param.project_species:
    csp.generate_reactionScores(project_param, project_species=[species])
