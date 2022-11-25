=======================================================
Welcome to the documentation for SBML2HYB
=======================================================

The sbml2hyb tool is an stand-alone executable application for SBML compatible hybrid modelling. The tool is written in Python and is intended as an interface to convert existing `SBML
<http://www.sbml.org>`_ models into a hybrid model (combines mechanistic equations and ML techniques). Below see the proposed pipeline in Figure 1.
The new internal hybrid model format HMOD (intermediate format — enables communication between the essential components of the mechanistic and hybrid models) can be translated to SBML and vice-versa. See `HMOD
<https://github.com/rs-costa/sbml2hyb/blob/main/models/chassagnole1standard.hmod>`_ format example.

.. figure:: images/Figure1.png
   :alt: Overview of the sbml2hyb pipeline

   **Figure 1. Overview of the sbml2hyb pipeline.**


Source code available `here
<https://github.com/r-costa/sbml2hyb>`_.

--------
Using SBML2HYB
--------
Here is an example of a SBML hybrid model (*Chassagnole* case study) built with **sbml2hyb**:

After launching sbml2hyb (see installation instructions), the following graphical user interface (GUI) will be open (Figure 2).
Once the simple GUI window opens, click the "Translate SBML file" button (see Figure 2), and browse to specify the SBML model file (here the mechanistic model example is taken from Biomodels database, `BIOMD0000000066
<https://www.ebi.ac.uk/biomodels/BIOMD0000000066#Files>`_) you want to convert.
Add then the information of the neural network component into the model (click "Add ML" button). Once you do this, select the "Inputs" (select all) and "Outputs" (vm5, vm4f, vm3f, vm2f, vm11, knadph and katpase) options, and the `Keras <https://github.com/r-costa/sbml2hyb/blob/main/models/Chass_Keras.h5>`_ neural network file for this case study (Figure 3) to be added to the mechanistic model. After this, click the "Confirm" buttons. Note: To generate the Keras H5 file that serves as a blueprint of the machine learning segment of the hybrid model, follow this `instructions <https://github.com/rs-costa/sbml2hyb/blob/main/models/keras_H5/instructions_createH5.txt>`_ or this example as `notebook <https://github.com/rs-costa/sbml2hyb/blob/main/models/keras_H5/create_keras_h5.ipynb>`_.
Finally, the hybrid model generated in HMOD format is reconverted in SBML by clicking the "Translate HMOD file" button and then "Confirm" button (Figure 4). 
To save the final hybrid SBML model file, click "Save file" button (Figure 5). 


.. figure:: images/Figure2.png
   :alt: The main GUI of sbml2hyb
   
   **Figure 2. The main GUI of sbml2hyb.**