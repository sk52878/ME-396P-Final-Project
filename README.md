# ME-396P-Final-Project
Repository for Engineering Application for Engineers Final Project

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
- settingsOpenSimAD.py from  and replace the file with the same name in UtilsDynamicSimulations > OpenSimAD from your OpenCap-Processing git clone (this does not need to be done, but lowers the convergence tolerance and mesh density of the optimizer to make convergence quicker and match the settings of the Google Colab code)
- colab_run.py

In colab_run.py, change the zip_path and trial variables to the exact path of your desired zip file and the name of the trial you would like to process
