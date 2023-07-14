**Purpose and Use Case**

The cellpaint package, an alternative for the MIT Ann Corpenter's group [Cellprofiler](https://github.com/CellProfiler/CellProfiler) package,
and it provide biologists and image analysts with simple analytic platform for phynotipic screening and drug discovery.
It takes in a 384 well-plate format set of tiff images, 
using JUMP Consortium Protocol which has 5 channels (C1 / C2 / C3 / C4 / C5) as
(nuclues / cytoplasm / nucleoli/ actin / mitochondria) painted with florescent dies
(DAPI / Concanavalin A / Syto14 / WGA+Phalloidin / MitoTracker). 
It's advantages are:


1) It can help with Design of Experiment (AssayPlates can study the effects of multiple treatments/dosages/cell-lines/densities).

2) Simple, easily tunable user-friendly interface for cellular segmentation (Check
   the [preview.ipynb](https://github.com/kazemSafari/cellpaint/blob/master/preview.ipynb) notebook.
   It possible to make both the biologist and the programmer/analysist can both be happy!).
   
3) It has two GPU-backended options for the initial segmentation of the nucleus and cell:
    [cellpose](https://github.com/MouseLand/cellpose) and [pycleranto](https://github.com/clEsperanto/pyclesperanto_prototype)
    
4) It then uses a novel method to match the segmentation of nucleus and cytoplasm, then
   uses the those two segmentation masks to segment the nucleoli and mitochondira as well.
   
5) Easy and simple interface to run

6) Extremely fast, 10-100X faster than [Cellprofiler](https://github.com/CellProfiler/CellProfiler),
   using standard desktop and not using any cloud computing resources.
   It takes about 6-9 hours to analyse a full 384-well plate of ```2000X2000``` pixel images, which is about 17000 images.
   (It uses pytorch/GPU as well as CPU-Multiprocessing for speedup).

8) It uses a torch-GPU implementation of the Wassertein Distance Map from each well from the DMSO condition,
   to get wellwise summary statistics.
   It help you decide on whether your control treatments as well as test treatments have worked.
   You can also use your own hit-calling methods on it Final Wassertein Distance MAP well summary stats.

**[Image Analysis Steps](https://github.com/kazemSafari/cellpaint/blob/master/main.py)**
1) Preview (Check and decide how happy you are with your segmentation on a few wells!)
2) Segmentation Step 1 (Segmenting nucleus and cell)
3) Segmentation Step 2 (Matching nucleus and cell segmentation as well as segmenting nucleoli and mitchondria)
4) Light-weight Feature extraction: Shape, Intensity, and Texture Features
5) Calcultes the Wassertein-Distance Map of each biological-well from the DMSO/Vehicle condition.

**Installation instructions**

To install cellpaint python package on a conda virtualenv called tensors:
1)	Install anacond3/miniconda3 on your windows or linux machine.
2)	Open an anaconda3 terminal:
3)	```conda create --name tensors python=3.10 --no-default-packages```
4)	```conda activate tensors```
5)	```python -m pip install cellpose --upgrade```
6) Only if you do have a dedicated Nvidia GPU available to you do the following:
```
pip uninstall torch
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
```
7)
	Option 1)
	
 	To install cellpaint directry from github:
	```
	pip install git+https://github.com/kazemSafari/cellpaint.git
	```
	
	Option 2)
	
 	To install cellpaint locally in your computer and in oder to be able to change it, 
	first download it from github to your computer,
	go to one directory above where your cellpaint folder is downloaded/located/saved, through
	an anaconda3 terminal, the stucture of directory would look like this:
	```
	dir/
	   cellpaint/
	            setup.py
	            README.md
	            cellpaint
	```
	type ```pip install -e cellpaint``` in the same terminal. The ```-e``` allows
   	one to edit the program.
   
All the required packages will be installed automatically from ```setup.py``` file! Done!
In case you are using a linux machine, you need to change all ```WindowsPath``` objects
In the code to ```PosixPath``` object.

Also if you are going to use Pycharm, its terminal might not recognize your anaconda3
virtualenv. Here is the fix from 
```https://stackoverflow.com/questions/48924787/pycharm-terminal-doesnt-activate-conda-environment```, 
if the pycharm terminal does not recognize your anaconda virtualenv, do the following:

Go to ```File -> Settings -> Tools -> Terminal```. Replace the value in ``Shell path`` with 
```cmd.exe "/K" path_to_your_miniconda3\Scripts\activate.bat tensors```.

Remember, you will be able to modify the content of this package 
only if you install it via Option 2).


**Running Cellpaint**

To learn how to use the program, go to [run_cellpaint.md](https://github.com/kazemSafari/cellpaint/blob/master/run_cellpaint.md).



