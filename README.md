# ME-396P-Final-Project
Repository for Engineering Application for Engineers Final Project

Gait Efficiency Scoring Site: https://testwebsitepy-hu95pzfrd4yxnpmexwz4ff.streamlit.app/

Full Gait Results Site: https://colab.research.google.com/drive/1l3eM42wMI94p1JGSOB8Yi6zufa7K-q9k

## To run Full Gait Results processing code locally:
Visit https://github.com/opencap-org/opencap-processing and follow the README

From this repo>AdditionalProcessing, download and place in the same directory as your cloned OpenCap-Processing files
- gait_analysis_edited.py
- FullProcessFunction.py
- settingsOpenSimAD.py from  and replace the file with the same name in UtilsDynamicSimulations > OpenSimAD from your OpenCap-Processing git clone (this lowers the convergence tolerance and mesh density of the optimizer to make convergence quicker, but this does not need to be changed to run the code)
Optional (to output the results as .csv files):
- FullGaitResults.ipynb
- colab_run.py

For results as pandas dataframes:
- Add unzipped OpenCap folder to same directory as all OpenCap-Processing files and make this your current working directory
- Call the FullProcess function from FullProcessFunction.py with the name of the desired session ID and name of the desired trial

For results as csv files:
- Download the optional files in addition to the other files
- Run FullGaitResults.ipynb and upload zipped folder when prompted
