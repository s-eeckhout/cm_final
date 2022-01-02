# Stroop-effect in ACT-R using CCMSuite

## Installation

In order to run the program python 2 is required.

Installing the required packages can be achieved using pip:
```bash
pip install ccmsuite/.
pip install numpy
pip install scipy
pip install matplotlib
pip install seaborn
```

## Usage
To run the ACT-R model that simulates the stroop-effect, the following must be run.
Every time you run the model the reaction times get saved into a file called 'RTcn.txt' or 'RTwr.txt', depending on the task used.
```bash
python2 myModel.py
```

To visualize the results
```bash
python datavisualisation.py
```