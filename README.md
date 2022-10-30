# SBML2HYB
## Overview
Hybrid modelling combine parametric functions (derived from knowledge) and nonparametric functions (derived from data) in the same model structure.
The sbml2hyb tool is an stand-alone executable application for [SBML](https://synonym.caltech.edu/) compatible hybrid modelling. The tool is written in Python and can be used for converting between SBML format and HMOD (intermediate format — enabling communication between the essential components of the mechanistic and hybrid models). See [HMOD](https://github.com/rs-costa/sbml2hyb/blob/main/models/chassagnole1standard.hmod) file example.

[![DOI](https://zenodo.org/badge/501372731.svg)](https://zenodo.org/badge/latestdoi/501372731)

## Quick start guide
### Installation
- Users have two options to install sbml2hyb:

(i) As a typical stand-alone executable Windows application; download the [files](https://drive.google.com/drive/folders/1yBpSaXts-D1bMXjq8MO6AbJkOjSibOji?usp=share_link). After saving the folder where you prefer on your computer, double-click the executable (.exe) file to open the tool. It works also on [Linux](falta link), and [MacOS](falta link) systems.

(ii) As a Python package (pip installer); run the following command via pip:
pip install -i https://test.pypi.org/simple/ sbml2hyb
- sbml2hyb is written in Python (requires version 3.8 or higher).
- Alternatively, you can clone this GitHub repository to a location on your computer's file system and then run sbml2hyb.py from the command-line.

After installing the package the user can simply import the library and call it. This is an example on how to use:

      import sbml2hyb as sb
      sb.main()

### Package Dependencies
- tkinter 3.10.7  
- Pillow 9.0  
- libsbml 5.19.6 
- Python 3.8.2
- Tensorflow 2.10.0

### Getting Started
#### How to use SBML2HYB:

The users can use sbml2hyb either via the command line interface or via a graphical user interface (GUI) that allows to convert SBML files into HMOD files and vice versa. 
Once the simple Graphical User Interface (GUI) window opens, click the "Translate SBML file" or "Translate HMOD file" button, to find the SBML or HMOD file you want to convert on the tool, respectively.  After few seconds, the user get the final output in the main panel of the GUI. The user can then save (click "export file" button) the final file (.xml or .hmod). 

Additionally, the user can adds information of the neural network component (optional) into the HMOD/SBML model format (first load a standard HMOD/SBML model file or after a first translate HMOD/SBML model step).  Click "Add ML" button  . Once the user do this, they need select the "inputs" and "outputs" options of the neural network, and the Keras H5 file (i.e., adding the ML component information). Click the "Confirm" button. Finally, the resulting hybrid model in HMOD (or SBML) format can then be reconverted in SBML (or HMOD), respectively. Click "Translate HMOD file" or "Translate SBML file" button. To generate an Keras H5 file that serves as a blueprint of the machine learning segment of a hybrid model, the Keras library from Tensorflow is used (see [instructions](https://github.com/rs-costa/sbml2hyb/blob/main/models/keras_H5/instructions_createH5.txt) and [code](https://github.com/rs-costa/sbml2hyb/blob/main/models/keras_H5/create_keras_h5.ipynb))


#### Creating a hybrid SBML model

Example: Park&Ramirez model

You can view the standard model SBML file input for this example in a [separate file](https://github.com/rs-costa/sbml2hyb/blob/main/models/parkramstandard.xml). The screenshot below (Figure 1) illustrates the output of the Park&Ramirez standard HMOD model after the SBML conversion. The user can also select the model "inputs" (S) and "outputs" (miu, vPM, VPT) options of the neural network, and the Keras H5 file (Figure 2) to convert directly to the hybrid model. You can view the resulting final hybrid HMOD file from the tool [here](https://github.com/rs-costa/sbml2hyb/blob/main/models/parkramhyb.hmod) and printscreens below (Figure 3). The hybrid model in HMOD format is then reconverted in the [hybrid SBML model](https://github.com/rs-costa/sbml2hyb/blob/main/models/parkramhyb.xml). 

<div align="center"> Figure 1. </div>

![alt text](https://github.com/rs-costa/sbml2hyb/blob/main/img/Figure1.PNG)

<div align="center"> Figure 2. </div>

![alt text](https://github.com/rs-costa/sbml2hyb/blob/main/img/Figure2.PNG)

<div align="center"> Figure 3. </div>

![alt text](https://github.com/rs-costa/sbml2hyb/blob/main/img/Figure3.png)

## Developed at
- NOVA School of Science and Technology, Universidade NOVA de Lisboa (since 2021)

## License
This work is licensed under a <a href="https://www.gnu.org/licenses/gpl-3.0.html"> GNU Public License (version 3.0).</a>
