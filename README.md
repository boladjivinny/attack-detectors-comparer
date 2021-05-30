**Attack detectors comparer** is a Python package which extend the [Botnet Detectors Comparer](http://downloads.sourceforge.net/project/botnetdetectorscomparer/BotnetDetectorsComparer-0.9.tgz)
tool by giving it a more flexible architecture, allowing the comparison technique presented in [1] to be used for a wider 
range of cybersecurity problems.

# Installation
## Dependencies
The package requires:

+ matplotlib
+ numpy
+ pandas>=1.2.4
+ scikit-learn>=0.24.2

## User installation
To install the package, run the following command:

```bash
pip install git+git@github.com:boladjivinny/attack-detectors-comparer.git
```

# Usage
**Attack detectors comparer**  comes bundled with an executable
module that generates a comprehensive output given the dataset.
For running it, it expects (1) an original file with a timestamp,
a source IP address and the corresponding security label and
(2) a file for each technique to be compared, with the predicted
labels for each of the technique in the relevant files.

The files are expected to be named after the technique. For instance,
if you have a technique called `Bayes`, the file should be
named `Bayes.csv` or with any other extension of your choice.
The said files are expected to only have one column, with more
likely to raise issues.

Below is a general guide on how to run the package:

```
usage: attack-detectors-comparer [-h] [-v] [-t {flow,time,weight}] [-T TIME] [-p {TPR,TNR,FPR,FNR,Precision,Accuracy,ErrorRate,FM1,FM2,FM05}] [-a ALPHA] [-c CSV] [-o OUT]
                               [-P PLOT_TO_FILE] [-l LABEL] [-L LABELS [LABELS ...]] [-g]
                               input predictions [predictions ...]

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later version.

positional arguments:
  input                 sorted input netflow labeled file to analyze (Netflow or Argus).
  predictions           the prediction files for each of the methods being evaluated

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         verbosity level (default: 0)
  -t {flow,time,weight}, --type {flow,time,weight}
                        type of comparison. Flow based (-t flow), time based (-t time), or weighted (-t weight). (default: flow)
  -T TIME, --time TIME  while using time based comparison, specify the time window to use in seconds. (default: 0)
  -p {TPR,TNR,FPR,FNR,Precision,Accuracy,ErrorRate,FM1,FM2,FM05}, --plot {TPR,TNR,FPR,FNR,Precision,Accuracy,ErrorRate,FM1,FM2,FM05}
                        defines the metric that should be plotted. (default: None)
  -a ALPHA, --alpha ALPHA
                        in weight mode, use this alpha for computing the score (default: 0.01)
  -c CSV, --csv CSV     print the final scores in csv format into the specified file. (default: None)
  -o OUT, --out OUT     store in a log file everything that is shown in the screen. (default: None)
  -P PLOT_TO_FILE, --plot-to-file PLOT_TO_FILE
                        instead of showing the plot on the screen, store it in a file.Type of plot given by the file extension. (default: None)
  -l LABEL, --label LABEL
                        the title of the column representing the label field. (default: Label)
  -L LABELS [LABELS ...], --labels LABELS [LABELS ...]
                        the labels available in the dataset (i.e. negative, positive, and optionally, background labels (default: ['normal', 'botnet'])
  -g, --generate-dummy-algos
                        whether to create the AllPositive and AllNegativealgorithms. (default: False)
```

# Citation
If you use this package in your work, please cite it as:

*In progress*

# Getting help
To get support regarding this package, please log an issue or shoot me an email
at vinny.adjibi@outlook.com and I will make sure to answer as soon as possible.
