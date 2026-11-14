#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 14:44:58 2026

@author: tyberns
"""

import os, shutil, sys, tempfile, zipfile
from FullProcessFunction import FullProcess

os.environ.setdefault("MPLBACKEND", "Agg")
AppDir = os.path.dirname(os.path.abspath(__file__))

zip_path, trial = sys.argv[1], sys.argv[2]

# Extract zip folder's contents into a temporary folder
tfolder = tempfile.mkdtemp(dir=AppDir)
with zipfile.ZipFile(zip_path) as z:
    z.extractall(tfolder)

# Read each entry in the extracted zip folder, while excluding additions from Mac or Linux if user recompresses folder
entries = [e for e in os.listdir(tfolder) if e != "__MACOSX" and not e.startswith(".")]

if len(entries) == 1 and os.path.isdir(os.path.join(tfolder, entries[0])):
    root, name = os.path.join(tfolder, entries[0]), entries[0]
else:
    root, name = tfolder, os.path.splitext(os.path.basename(zip_path))[0]
session_id = name.replace("OpenCapData_", "")

# Setup the directory for the kinematics/metrics process
link_dir = os.path.join(AppDir, name)

# Setup the directory for the dynamics process
session_dir = os.path.join(AppDir, session_id)

shutil.move(root, session_dir)
os.symlink(session_dir, link_dir)

outputs = FullProcess(session_id, trial)

titles = ["Gait_metrics", "Joint_moments", "Ground_reaction_forces",
          "Hip_extensors", "Hip_abductors", "Hip_flexors", "Hamstrings",
          "Quadriceps", "Plantarflexors", "Dorsiflexors"]

os.makedirs("results", exist_ok=True)
for title, df in zip(titles, outputs):
    df.to_csv(os.path.join("results", title + ".csv"))
print("DONE")