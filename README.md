# A Reference Data Set for the Study of Healthy Subject Gait with Inertial Measurements Units 

## Context and dataset

This repository provides a dataset in the folder "GaitData" consisting of 110 multivariate gait signals collected using three inertial measurement units (MTw Awinda XSens, one on each foot and one on the lower back at the level of the fifth lumbar vertebra). The data was obtained from a sample of 19 healthy subjects who followed a predefined protocol: standing still, walking 10 meters, turning around, walking back, and stopping. 

This dataset also contains extensive signal metadata, including the start and end timestamps of each footstep, along with contextual information for each trial and subject (age, gender, weight). 

Gait events correspond to stride delimitations provided with two previously validated algorithms from the literature []. All these detections were then manually checked. 

Files are identified by their filename, which associates the number dedicated to the subject and the number of the trial. The filename for the third trial of the second subject is 2-3.
- For the trunk sensor: [filename]_lb.txt;
- For the right foot sensor: [filename]_rf.txt;
- For the left foot sensor: [filename]_lf.txt;
- For the metadata: [filename]_meta.json. 

## Demo and accessibility 

The data provided in this repository are described in the following article: XXXXXXXXXXX
Please cite this article whenever you want to make a reference to this data set.
A simple online exploration tool is available online. Data can be downloaded as a zipped archive (GaitData.zip, ~30MB). 

Once extracted, the data can be read using the following code snippets (main.py, in Python 3.8). Be sure to execute those lines while in the same directory as the extracted GaitData folder.

