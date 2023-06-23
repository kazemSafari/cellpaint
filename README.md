**Purpose and Use Case**

The cellpaint package, an alternative for the MIT Ann Corpenter's group [Cellprofiler](https://github.com/CellProfiler/CellProfiler) package,
and it provide biologists and image analysts with simple analytic platform for phynotipic screening and drug discovery.
It takes in a 384 well-plate format set of tiff images, 
using JUMP Consortium Protocol which has 5 channels (C1 / C2 / C3 / C4 / C5) as
(nuclues / cytoplasm / nucleoli/ actin / mitochondria) painted with florescent dies
(DAPI / Concanavalin A / Syto14 / WGA+Phalloidin / MitoTracker). 
It's advantages are:
0) It can with Design of Experiment 
(Have multiple treatments/dosages/cell-lines/densities).
1) Simple, easily tunable user-friendly interface for cellular segmentation (Check
   the [preview.ipynb](https://github.com/kazemSafari/cellpaint/blob/master/preview.ipynb) notebook.
   It possible to make both the biologist and the programmer/analysist can be happy,
   less arguments inside your team on who knows more,
   the biologist or the analyst! Neither! Stop arguing!).
2) It has two GPU-backended options for the initial segmentation of the nucleus and cell:
   
    [cellpose](https://github.com/MouseLand/cellpose) and [pycleranto](https://github.com/clEsperanto/pyclesperanto_prototype)
4) It then uses a novel method to match the segmentation of nucleus and cytoplasm, then
   uses the those two segmentation masks to segment the nucleoli and mitochondira as well.
5) Easy and simple interface to run
7) Extremely fast, 10-100X faster than [Cellprofiler](https://github.com/CellProfiler/CellProfiler), using standard desktop and not using any cloud computing resources.
   (Uses pytorch/GPU as well as CPU-Multiprocessing for speedup).
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
	Option 1) To install cellpaint directry from github:
	```
	pip install git+https://github.com/kazemSafari/cellpaint.git
	```
	
	Option 2) To install cellpaint locally in your computer and in oder to be able to change it, 
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
   
All the required packages will be installed automatically from setup.py file! Done!
In case you are using a linux machine, you need to change all WindowsPath objects
In the code to PosixPath object.

Also if you are going to use Pycharm, its terminal might not recognize your anaconda3
virtualenv. Here is the fix from 
```https://stackoverflow.com/questions/48924787/pycharm-terminal-doesnt-activate-conda-environment```:
If the pycharm terminal does not recognize your anaconda virtualenv, do the following:
Go to ```File -> Settings -> Tools -> Terminal```. Replace the value in ``Shell path`` with
```
cmd.exe "/K" path_to_your_miniconda3\Scripts\activate.bat tensors
```
Remember, you can only modify the program if you install it using Option 2).

**Preparations for running it on a different sample plate than YOKO/PerkimElmer**

(modifications needed to be applied to ```cellpaint/cellpaint/steps_single_plate /step0_args.py```):
The structure of the directory of your data/images/plate has to be as follows:
```
Experiment_Name\
	Images_folder_Name\
		Your image tiff files
	Platemap.xlsx
```
1)	Make sure the platemap file is in the same directory as your image files.
You need to make sure that your platemap format follows our empty template ```platemap_template.xlsx``` protocol.
Make sure to fill out all these sheets properly:
```
Treatment
CellLine
Dosage
Density
Other
Anchor
Control
```
2)	If you are not using the PerkinElmer plate protocol you, or your images format is not 5 channels 
You need to update the ```sort_key_for_imgs``` function inside the 
```cellpaint/cellpaint/steps_single_plate /step0_args.py``` file. So that our cellpaint package knows 
how to extract the necessary metadata from each individual tiff file inside that image folder which are:
```
folder: The name of the image folder containing your tiff files
filename: the name of the tiff file which should be passed in as a WindowsPath/PosixPath object 
if you are using Windows/Linux respectively.  
well_id: The image filename should contain the well-id of that plate where the image tiff file is taken from.
fov: The image should contain the fov of that well where the image tiff file is taken from.
channel: Which die/channel does the image correspond to.
```
In the YOKO/PerkinElmer protocol There are 5 channels corresponding to:
```
self.args.channel_dies = {
    "C1": "DAPI",  # nucleus
    "C2": "Concanavalin A",  # cyto
    "C3": "Syto14",  # nucleoli
    "C4": "WGA+Phalloidin",  # actin
    "C5": "MitoTracker",  # mito}
```

Example:
```
elif plate_protocol == "combchem":
    """img filename example:
    .../P000025-combchem-v3-U2OS-24h-L1-copy1/
    P000025-combchem-v3-U2OS-24h-L1-copy1_B02_s5_w3C00578CF-AD4A-4A29-88AE-D2A2024F9A92.tif"""
    folder = file_path.parents[1].stem
    filename = file_path.stem
    split = filename.split("_")
    well_id = split[1]
    fov = split[2][1]
    channel = split[3][1]
```

3)	Also, if your image folder may contain tiff other than the image files you need to figure out 
a way to filter them similar to how it is done for perkim-elmer.
You may also need to provide the necessary sorting functions to sort the channels properly,
depending on how your microscope saves image filenames:
```
if self.args.plate_protocol.lower() in ["perkinelmer", "greiner"]:
    # sometimes there are other tif files in the experiment folder that are not an image, so we have to
    # remove them from img_paths, so that they do not mess-up the analysis.
    self.args.img_filepaths = list(
        filter(lambda x: x.stem.split("_")[-1][0:5] == "T0001", self.args.img_filepaths))
self.args.img_filepaths = sorted(
    self.args.img_filepaths,
    key=lambda x: sort_key_for_imgs(x, "to_sort_channels", self.args.plate_protocol))
```

**Modifying the program**

1)	Add your plate full filepath and folder name to the pairs variable inside 
```cellpaint/cellpaint/main.py``` file. Example:
```("image_folder_a", "path_to_image_folder_a"),```
 
2)	Choose your hyperparameters for segmentation after playing around with them in
```cellpaint/cellpaint/steps_single_plate /preview.ipynb```. Those hyperparamters are as follows:
2-1) The index ```(0, 1, 2, 3, 4, 5 in YOKO/PerkinElmer)``` of each channel in the 
images as well as the number of fov taken per well in the plate:
```
self.args.nucleus_idx = nucleus_idx
self.args.cyto_idx = cyto_idx
self.args.nucleoli_idx = nucleoli_idx
self.args.actin_idx = actin_idx
self.args.mito_idx = mito_idx
self.args.n_fovs_per_well = n_fovs_per_well
```
2-2) Rescale intensity lower and upper bounds for each channel:
```
self.args.rescale_intensity_bounds = {
    "w1": w1_intensity_bounds,
    "w2": w2_intensity_bounds,
    "w3": w3_intensity_bounds,
    "w4": w4_intensity_bounds,
    "w5": w5_intensity_bounds,}
```
2-3) Whether to choose background subtraction and the radius of background subtraction ball for each channel:
```
self.args.bg_sub = False
w1_bg_rad, w2_bg_rad, w3_bg_rad, w4_bg_rad, w5_bg_rad
```
2-4) Cellpose and Thresholding segmentation parameters, which are needed to be adjusted depending on the cell-line:

**Cellpaint Step 2) that can be tuned to the plate and image dimensions**
```
self.args.cellpose_nucleus_diam = cellpose_nucleus_diam
self.args.cellpose_cyto_diam = cellpose_cyto_diam
self.args.cellpose_batch_size = cellpose_batch_size
self.args.cellpose_model_type = cellpose_model_type
self.args.min_sizes = {
    "w1": w1_min_size,
    "w2": w2_min_size,
    "w3": w3_min_size,
    "w5": w5_min_size,}
```

**Cellpaint Step 3) argumnets that can be tuned to the plate**
```
# w2/cyto hyperparameters
self.args.multi_nucleus_dist_thresh = multi_nucleus_dist_thresh
# w3/nucleoli segmentation hyperparameters
self.args.min_nucleoli_size_multiplier = min_nucleoli_size_multiplier
self.args.max_nucleoli_size_multiplier = max_nucleoli_size_multiplier
self.args.nucleoli_bd_area_to_nucleoli_area_threshold = nucleoli_bd_area_to_nucleoli_area_threshold
self.args.w3_local_rescale_intensity_ub = w3_local_rescale_intensity_ub
# w5/cyto segmentation hyperparameters
self.args.w5_local_rescale_intensity_ub = w5_local_rescale_intensity_ub
```
After choosing the propriate ones, pass them in to the Args class inside the ```cellpaint/cellpaint/main.py``` file. 
You can create a custom function for it, similar to ```set_default_datasets_hyperparameters```.
After, defining your own ```set_custom_datasets_hyperparameters``` 
function or whatever you call, replace the line ```set_default_datasets_hyperparameters(args)``` 
below with your own custom function.
```
args = Args(experiment=exp_fold, main_path=main_path, mode="full").args
# args = set_default_datasets_hyperparameters(args)
args = set_custom_datasets_hyperparameters(args)
main_worker(args)
```

**Running the program**

After making sure all the necessary adjustments are made.
Copy main.py file to your desired filepth location.
Add your plate full filepath and folder name to the pairs variable inside ```cellpaint/cellpaint/main.py``` 
file. Example:
```("image_folder_name", "path_to_the_image_folder"),```
Open an anaconda terminal and run the following commands:
```
conda activate tensors
```
Modify ```main.py``` by passing in your own ```experiment_path```, ```experiment_folder``` and your own 
```args=set_custom_datasets_hyperparameters(args)``` hyperparameters.:
```
if __name__ == "__main__":
    experiment_path = WindowsPath(r"path_to_your_experiment_folder_excluding_the_experiment_folder_itself")
    experiment_folder = WindowsPath(r"your_experiment_folder")
    # entry point of the program is creating the necessary args
    start_time = time.time()
    args = Args(experiment=experiment_folder, main_path=experiment_path, mode="full").args
    # args = set_default_datasets_hyperparameters(args)
    # args = set_custom_datasets_hyperparameters(args)
    main_worker(args)
    print(f"program finished analyzing experiment {args.experiment} in {(time.time()-start_time)/3600} hours ... ")
```
Also, make sure the platemap excel file is filled-in properly,
and is in the same directory as ```experiment_path```.
Run the program in a conda terminal using:
```
python main.py
```

