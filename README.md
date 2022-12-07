# Rehab-Demo-Pipeline
This repository contains the code for the demo of Physical Disability Rehabilitation Process (work in progress).

# TODOs Checklist
- [ ] Converters:
  - [x] Lab Kinect to NTU
  - [x] Kimore to NTU
  - [x] Live Feed to NTU
  - [ ] UIPRMD to NTU (?)
- [ ] Add models to the pipeline
  - [x] M3D
  - [ ] STGCN
- [ ] GUI
  - [x] Select folder option
  - [x] Record data and use it in conversion and model inference
  

# Instructions
Since this is a work in progress, the folder structure will change over time. However, the core structure is as follows:

```
├── data_format_visualizer (a Jupyter notebook that visualizes the data formats) 
├── old_code (The previous code as well as the data from the DTW paper)
  ├── data (The mat files of the lab kinect data)
  ├── ...
├── README.md
├── requirements.txt
├── src (The converters and GUI will live here)
```

### Setting up development environment
The project only works on Windows 10 since the entirety of the project stands on XBOX Kinect v2, which does not work without Windows.

The project depends on (as of Nov 04, 2021):
- PyQt5
- Numpy
- Scipy
- Matplotlib
- TQDM (only during initial development phases with command line usage)
- Black (The code formatter, more details below)
- PyTorch
- Kinect SDK v2.0 [link](https://www.microsoft.com/en-us/download/details.aspx?id=44561)

It is recommended that you use Anaconda and create a separate environment, however `virtualenv` is also fine (but not tested). Use the `requirements.txt` file to install the needed dependencies. 

```
pip install -r requirements.txt
```

### Code Formatting
The project uses Black as its formatter. To avoid merge conflicts, it is recommended that the contributors use Black formatter along with a standard code editor such as VSCode or Sublime Text. You can get started with it [here](https://github.com/psf/black). For setting up VSCode to use Black, you can find instructions [here](https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0).
  
# Data Formats
The data formats (.skeleton, lab kinect data etc) are described in [this document](https://docs.google.com/document/d/1SiD93TSvSQpORiyGl64fl5Y48TjgP75CURzr45zoPsg/edit)
