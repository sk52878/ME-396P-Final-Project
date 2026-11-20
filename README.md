# ME-396P-Final-Project
Repository for Engineering Application for Engineers Final Project

Use OpenCapData_99d7534a-b172-4908-9d41-2fd47289be97_cff85028-d71b-4ce6-acbb-0960630eb719.zip in the root directory for testing.

Presentation: https://docs.google.com/presentation/d/1j-i9rDVvU3zblhlkTz57k1LNPg1J9USr/edit?usp=sharing&ouid=116060017966637902852&rtpof=true&sd=true

Gait Efficiency Scoring Site: https://testwebsitepy-hu95pzfrd4yxnpmexwz4ff.streamlit.app/

Full Gait Results Site: https://colab.research.google.com/drive/1l3eM42wMI94p1JGSOB8Yi6zufa7K-q9k

## To run Full Gait Results processing code locally:
Visit https://github.com/opencap-org/opencap-processing and follow the "Install requirements" section of the README
- Skip the OpenCap login step (step 9)
- Run conda install ipykernel in this environment (this is most likely already installed, but should be done as a check)

From this repo>AdditionalProcessing, download and place in the same directory as your cloned OpenCap-Processing files:
- gait_analysis_edited.py
- FullProcessFunction.py
- colab_run.py

From this repo>AdditionalProcessing, download and replace the same-named files in the same directory as your cloned OpenCap-Processing files:
- utils.py
- utilsProcessing.py

From this repo>AdditionalProcessing>UtilsDynamicSimulations>OpenSimAD, download these files and replace the current files with the same name under the same folder path
- utilsOpenSimAD.py
- settingsOpenSimAD.py (this does not need to be done, but lowers the convergence tolerance and mesh density of the optimizer to make convergence quicker and match the settings of the Google Colab code)

In colab_run.py, change the zip_path and trial variables to the exact path of your desired zip file and the name of the trial you would like to process

Notes:
- Before running the local code more than once, all files in opencap-processing>UtilsDynamicSimulations>OpenSimAD>build-ExpressionGraphF must be deleted
- If processing multiple trials (or the same trial multiple times) from the same session, folders "OpenCapData_{SessionID}" and "{SessionID}" must be renamed, deleted, or moved out of your current working directory.
- The processing function is built to quit if it cannot converge after 5000 iterations. If this occurs, try again with a different trial from the same session.
