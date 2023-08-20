# FcFuzzer

This artifact corresponds to the research paper titled "Detecting Interpreter Bugs via Filling Function Calls in Skeletal Program Enumeration." In this paper, we introduce the proposed automated fuzzing tool, i.e., FcFuzzer. FcFuzzer, developed in Python 3, serves two primary functions: first, it generates test programs using an enumeration approach, and second, it tests these generated programs through differential methods. An advantageous aspect of FcFuzzer, in comparison to the existing skeletal program enumeration tool, is its capacity to facilitate function call enumeration. This functionality brings about diverse call dependencies within the generated test programs.

## Artifact Description
FcFuzzer is implemented as a Python program that takes a target Python interpreter, a reference Python interpreter, and a set of seed programs as the inputs and outputs a set of test programs triggering interpreter bugs.

The implementation of FcFuzzer consists of two parts: program generation and program execution. In the stage of program generation, 
FcFuzzer incorporates the enumeration of function calls into the SPE process and hence exhaustively derives non-alpha-equivalent test programs with diverse call dependencies.
In the stage of program execution, FcFuzzer detects bugs via differential testing. The interpreter invokes os.system() in the _os_ module to execute test programs. The function os.system() returns an operating system code, indicating the status of program execution. Bugs are identified by performing a differential comparison of these system codes.

The FcFuzzer project contains the following content:

- **README.md**: This file provides essential information about FcFuzzer, including execution requirements, installation instructions, and output details.

- **dataset**: All seed programs are put in this directory. Currently, this directory contains three subdirectories: "test_function", "seed_dataset", and "seeds_triggering_unknown_bugs". The "test_function" subdirectory holds seed programs for evaluating the enumeration capability of function calls. "seed_dataset" includes all seed programs used in the experiments. The "seeds_triggering_unknown_bugs" subdirectory contains several sampled seed programs to reproduce unknown bugs. 

- **error**: This directory will store all the test programs that triggered bugs during the experiments.

- **log**: This directory contains log files documenting the enumeration process for each seed program.

- **algorithm.py**, ast_analysis.py, ast.transform.py: These three files provide fundamental functions, including AST analysis, essential for the enumeration process.

- **run.py**: This file serves as the light version of the entry point for FcFuzzer. This file does not apply differential testing and can only detect crash bugs.

- **run_differential.py**: This file is the primary entry point for FcFuzzer. This file contains differential testing to identify behavioral bugs and miscompilation bugs.

- **Python3.9.0.zip**: This zip file encompasses the source code of CPython 3.9.0.




## Environment Setup

We have experimented FcFuzzer on both Ubuntu and Mac OS. FcFuzzer can work well on these two operating systems.  Our experiments were conducted on a computer with Intel® Core™ i7-6700 CPU @ 3.40GHz × 8 and 15.6 GiB memory under Ubuntu 18.04.3 LTS 64-bit.   

To execute FcFuzzer successfully, we must use Python version (CPython) 3.9.0 or higher. Using an earlier version of CPython could lead to an error message such as "'FunctionDef' object has no attribute 'end_lineno'", a consequence of the _end_lineno_ attribute being introduced after CPython 3.9.0.

For obtaining the required Python interpreters, we have two options. We can download them directly from the official CPython website: https://www.python.org/. Alternatively, we can utilize the provided **Python3.9.0.zip** file. The installation of CPython 3.9.0 can be completed as follows:


To install the required Python dependencies, we need to execute the following commands in the console:


      sudo apt-get install build-essential gdb lcov pkg-config 
      libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
      libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
      lzma lzma-dev tk-dev uuid-dev zlib1g-dev


To install CPython 3.9.0, we need to utilize the following commands:


      cd Python3.9.0;
      ./configure;
      make;
      sudo make install

Apart from the Python interpreter, the third-party library "wrapt-timeout-decorator" is also essential for managing timeouts. To install this module, we need to execute the following command:

      python3.9 -m pip install wrapt-timeout-decorator

or 

     sudo pip install wrapt-timeout-decorator


## Getting Started

To execute FcFuzzer, we need to navigate to the working directory "FcFuzzer":

      cd FcFuzzer;


Before we launch FcFuzzer, we need to specify the target Python interpreter, i.e., the Python interpreter that needs to be tested.
Specifically, we need to update the statement "interpreter = 'python3.9'" (line 298 of "run.py" and lines 331 and 332 of "run\_differential.py"). We need to replace 'python3.9' in this statement with the path of the target Python interpreter. For instance, if we want to test RustPython 0.2.0 interpreter and have installed it, we need to replace  the statement "interpreter = 'python3.9'" with the statement "interpreter = 'rustpython'".

We also need to specify the path of seed programs. All seed programs should be put in the directory "dataset". Thus, we need to specify the path of seed programs. For instance, in "run.py" and "run\_differential.py", we can replace the statement  "tdir = os.getcwd() + '/dataset'" with the statement "tdir = os.getcwd() + '/dataset/test\_function'". At this time, all seed programs in the directory 'test\_function' will be used. 


After we specify the path of interpreters and the path of the seed programs, we can launch FcFuzzer using the command:

      python run.py 

or running it with differential testing:

      python run_differential.py


The console displays all generated test programs and their execution results using the specified Python interpreter.
To assess FcFuzzer's functionality, we could configure the path of seed programs as "tdir = os.getcwd() + '/dataset/test\_function'' in "run.py" and configure the target Python interpreter as CPython 3.9.0. Subsequently, we run FcFuzzer and observe the generated test programs. Crashes will be stored in the **error** directory. 


## Reproducibility Instructions
 
Running the whole experiment is time-consuming. We spent one month fuzzing the interpreters with all seed programs in the dataset. Alternatively, we can reproduce the found bugs with proper seed programs. 
For instance, we can use the seed programs in "seeds\_triggering\_unknown\_bugs" directory to reproduce some unknown bugs documented in the paper.
To reproduce unknown bugs, we need to configure the path of seed programs as "tdir = os.getcwd() + '/dataset/seeds\_triggering\_unknown\_bugs'' and the Python interpreter as CPython 3.9.0. Then we run them with FcFcuzzer. The crashing test programs will be stored in **error** directory. 



