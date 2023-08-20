# FcFuzzer

### This repository is for paper "Detecting Interpreter Bugs via Filling Function Calls in Skeletal Program Enumeration"


### Introduction of this repository

In this repository, we provide the source code for the proposed tool FcFuzzer and the reproduction tool Com_SPE, i.e., the state-of-the-art combinatorial SPE. Additionally, we include the results of the first experiment, which consists of 10 repeated experiments. The experiment results contain all the generated test programs, the number of programs triggering bugs, the number of discovered bugs, and coverage information. Sampled seeds include all sampled seeds in the first experiments. 



### Preparation

Python version: 3.9.0+ or you may receive a error message "'FunctionDef' object has no attribute 'end_lineno'"




download source code of python 3.9.0 or extract the provided zip file "python3.9.0.zip", then use the following commands to make the stardard installation:

"""
cd python3.9.0 
./configure
make 
make install
"""


python3.9.0 interpreter is taken as the default test target. 

If you have installed other tested Python interpreters, feel free to modify the Python interpreter path in "run.py", change "interpreter = os.getcwd() + '/Python3.9.0/python' "  into your own python 


Next, you need to return to the work directory with "cd .."


Now your work directory is "FcFuzzer", three directories, i.e., dataset, error,log, in this working directories.



### Install the package to handle timeout. 

use the installed python interpreter to install module.

"./python3.9.0/python -m pip install wrapt-timeout-decorator"

or "./python3.9.0/python.exe -m pip install wrapt-timeout-decorator"(mac OS)



 



### Running tools

To run FcFuzzer and Com_SPE, you need to enter the working directory.  



<!-- Next, you can configure the tested interpreter by replacing the configure of "interpreter" in  FcFuzzer/run.py  with the path of tested interpreters. -->


Then you can run the tool by commands, e.g., "python3.10 run.py"

### Note
The differential testing is optional in this tool.
If you just want to detect crash bugs, try the default "run.py" with the steps in "Running tools". It is fast.
If you wish to detect crash bugs, behavior bugs, and miscompilation bugs, try "run_differential.py" with the same steps.





