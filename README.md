# FcFuzzer

### This repository is for paper "Detecting Interpreter Bugs via Filling Function Calls in Skeletal Program Enumeration"


### Introduction of this repository

In this repository, we provide the source code for the tool FcFuzzer and the reproduction tool Com_SPE, i.e., the state-of-the-art combinatorial SPE. Additionally, we include the results of the first experiment, which consists of 10 repeated experiments. The experiment results contain all the generated test programs, the number of programs triggering bugs, the number of discovered bugs, and coverage information. Sampled seeds include all sampled seeds in the first experiments. 



### Running tools
To run FcFuzzer and Com_SPE, you need first enter the working directory.  

e.g., cd FcFuzzer/Com_SPE



Then you need to configure  dataset path.

e.g. place your seed test programs FcFuzzer/dataset and  modify the definition of variable "tdir" in FcFuzzer/run.py as the absolute path in your computer.



Next, you can configure the tested interpreter by replacing the configure of "interpreter" in  FcFuzzer/run.py  with the path of tested interpreters.



Finally, you can run the tool by commands "python run.py"

### Note
The differential testing is optional in this tool.
If you just want to detect crash bugs, try the default "run.py" with the steps in "Running tools". It is fast.
If you wish to detect crash bugs, behavior bugs, and miscompilation bugs, try "run_differential.py" with the same steps.
 




