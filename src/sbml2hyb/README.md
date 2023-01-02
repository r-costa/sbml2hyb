# Source code files

This folder contains the code for the tool, in the following files:

- "sbml2hyb.py" -> This is the code main file where the pipeline is executed.
- "Hmod.py" -> A class that builds the structure of the proposed format HMOD
- "hmod_parser.py" -> A script that parses HMOD files into XML files
- "hmod_validator.py" -> A script that validates HMOD files
- "neural_network_parser.py" -> A script to parse ML components
- "xml_parser.py" -> A script to parse XML files into HMOD
- "xml_validator.py" -> A script that validates XML files

Additionally, the code to generate the windows executable is also made available in the "create_executable_windows.py" file. To create the executable:

1. Open Command prompt window in this folder.
2. Execute the following command: "pip install --upgrade cx_Freeze Pillow tensorflow python-libsbml".
3. Execute the following command: "python create_executable_windows.py build".


