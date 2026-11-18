#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 17:36:51 2026

@author: tyberns
"""

## The file identification needs to be changed, as it will be read in from the 

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## Helper Functions

def read_mot(path):
    # Find the line where the header ends
    with open(path, "r") as f:
        for i, line in enumerate(f):
            if line.strip().lower() == "endheader":
                header_rows = i + 1
                break
        else:
            raise ValueError(f"No 'endheader' found in {path}")

    df = pd.read_csv(path, sep=r"\s+", skiprows=header_rows)
    return df

def load_dynamics(tol, mesh):
    kinetics = read_mot(f"Test - {tol}-{mesh}/OpenSimData/Dynamics/walk1/kinetics_walk1_0.mot")
    kinetics = kinetics[['time', 'hip_flexion_r_moment', 'hip_adduction_r_moment', 'hip_rotation_r_moment', 'knee_angle_r_moment', 'ankle_angle_r_moment', 
                         'hip_flexion_l_moment', 'hip_adduction_l_moment', 'hip_rotation_l_moment', 'knee_angle_l_moment', 'ankle_angle_l_moment']]
    
    grfs = read_mot(f"Test - {tol}-{mesh}/OpenSimData/Dynamics/walk1/GRF_resultant_walk1_0.mot")
    
    muscles = read_mot(f"Test - {tol}-{mesh}/OpenSimData/Dynamics/walk1/forces_walk1_0.mot")
    muscles = muscles[['time', 'bflh_l', 'bfsh_l', 'gaslat_l', 'gasmed_l', 'glmax1_l', 'glmax2_l', 'glmax3_l', 'glmed1_l', 'glmed2_l', 'glmed3_l', 'glmin1_l', 'glmin2_l', 'glmin3_l', 'psoas_l', 'recfem_l', 'semimem_l', 'soleus_l', 'tibant_l', 'vasint_l', 'vaslat_l', 'vasmed_l', 
                      'bflh_r', 'bfsh_r', 'gaslat_r', 'gasmed_r', 'glmax1_r', 'glmax2_r', 'glmax3_r', 'glmed1_r', 'glmed2_r', 'glmed3_r', 'glmin1_r', 'glmin2_r', 'glmin3_r', 'psoas_r', 'recfem_r', 'semimem_r', 'soleus_r', 'tibant_r', 'vasint_r', 'vaslat_r', 'vasmed_r']]

    return kinetics, grfs, muscles

def resample_to_ref(ref_df, test_df):
    t_ref = ref_df["time"].to_numpy()
    t_test = test_df["time"].to_numpy()
    mask = (t_ref >= t_test.min()) & (t_ref <= t_test.max())
    t = t_ref[mask]
 
    cols = [c for c in ref_df.columns if c != "time"]
    ref = ref_df.loc[mask, cols].to_numpy()
    test = np.column_stack([np.interp(t, t_test, test_df[c].to_numpy())
                            for c in cols])
    return t, cols, ref, test
 
 
def signal_metrics(t, ref, test):
    """Metrics for one signal (1-D arrays on the same time base)."""
    err = test - ref
    rng = ref.max() - ref.min()
    rmse = np.sqrt(np.mean(err ** 2))
 
    i_ref, i_test = np.argmax(np.abs(ref)), np.argmax(np.abs(test))
    peak_ref, peak_test = ref[i_ref], test[i_test]
    peak_den = max(abs(peak_ref), 1e-9)
 
    return {
        "rmse": rmse,
        "nrmse_pct": 100 * rmse / rng if rng > 1e-9 else np.nan,
        "max_abs_err": np.max(np.abs(err)),
        "peak_err_pct": 100 * abs(peak_test - peak_ref) / peak_den,
        "peak_time_err_s": t[i_test] - t[i_ref],
    }
 
 
def compare_group(ref_df, test_df):
    """Per-signal metrics DataFrame for one group (moments/grfs/muscles)."""
    t, cols, ref, test = resample_to_ref(ref_df, test_df)
    rows = {c: signal_metrics(t, ref[:, j], test[:, j])
            for j, c in enumerate(cols)}
    return pd.DataFrame(rows).T

tol = np.array([2, 3])
density = np.array([20, 30, 50, 75, 100])
runtime = np.array([[1.43, 3.84, 12.91, 10.93, 15.04],
                    [3.22, 4.30, 11.13, 15.49, 21.71]])

ctrl = (3, 100)   # (tol, mesh) used as the reference
groups = ("kinetics", "grfs", "muscles")

control = dict(zip(groups, load_dynamics(*ctrl)))
control["runtime (min)"] = runtime[1][4]

per_signal = []   # long-format: run, group, signal, metrics...
summary = []      # one row per run

for i,t in enumerate(tol):
    for j,mesh in enumerate(density):
        
        if (t, mesh) == ctrl:
            continue   # skip comparing the control to itself
        
        test = dict(zip(groups, load_dynamics(t, mesh)))
        
        row = {"run": f"Test - {t}-{mesh}"}
    
        for group in ("kinetics", "grfs", "muscles"):
            m = compare_group(control[group], test[group])
            m.insert(0, "group", group)
            m.insert(0, "run", f"Test - {t}-{mesh}")
            per_signal.append(m.reset_index(names="signal"))
 
            row[f"{group}_nrmse_mean"] = m["nrmse_pct"].mean()
            row[f"{group}_nrmse_max"] = m["nrmse_pct"].max()
            row[f"{group}_peak_err_max"] = m["peak_err_pct"].max()
            row["runtime_(min)"] = runtime[i][j]
            
        summary.append(row)
        
per_signal = pd.concat(per_signal, ignore_index=True)
summary = pd.DataFrame(summary)
summary = summary.sort_values(by="runtime_(min)")

os.makedirs("comparison_results", exist_ok=True)
per_signal.to_csv("comparison_results/per_signal_metrics.csv", index=False)
summary.to_csv("comparison_results/run_summary.csv", index=False)
    
pd.set_option("display.width", 200, "display.max_columns", 30)
print("\n=== Run summary ===")
print(summary[["run", "kinetics_nrmse_max", "grfs_nrmse_max", "muscles_nrmse_max", "runtime_(min)"]].round(2).to_string(index=False))

# Worst-offending signals overall (useful for muscle forces)
print("\n=== 5 worst signals by NRMSE (all runs) ===")
print(per_signal.nlargest(5, "nrmse_pct")[["run", "group", "signal", "nrmse_pct", "peak_err_pct"]].round(2).to_string(index=False))
        
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

xpos, ypos = np.meshgrid(np.arange(len(tol)), np.arange(len(density)), indexing='ij')
xpos = xpos.ravel()
ypos = ypos.ravel()
zpos = np.zeros_like(xpos)

dx = dy = 0.6
dz = runtime.ravel()

ax.bar3d(xpos - dx/2, ypos - dy/2, zpos, dx, dy, dz,
         shade=True, color='skyblue')

# Label ticks with the real values
ax.set_xticks(np.arange(len(tol)))
ax.set_xticklabels([r'$10^{-2}$', r'$10^{-3}$'])
ax.set_yticks(np.arange(len(density)))
ax.set_yticklabels(density)

ax.set_xlabel('Tolerance')
ax.set_ylabel('Mesh Density')
ax.set_zlabel('Runtime (min)')
plt.show()