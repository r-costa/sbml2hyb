from cx_Freeze import setup, Executable

setup(
    name="SBML2HYB",
    version="1.0.1",
    description="DESCRIPTION",
    options={
        "sbml2hyb": {"packages": ["Pillow", "tensorflow", "tkinter", "python-libsbml"]}
    },
    executables=[Executable("sbml2hyb_exe.py", base="Win32GUI")],
)
