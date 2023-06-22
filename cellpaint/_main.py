import time
from pathlib import WindowsPath
import cv2

from cellpaint.steps_single_plate.step0_args import Args
from cellpaint.steps_single_plate.step1_segmentation_preview import preview_run_loop
from cellpaint.steps_single_plate.step2_segmentation_p1 import step2_main_run_loop
from cellpaint.steps_single_plate.step3_segmentation_p2 import step3_main_run_loop
from cellpaint.steps_single_plate.step4_feature_extraction import step4_main_run_loop
from cellpaint.steps_single_plate.step5_distance_map_with_torch_api import WellAggFeatureDistanceMetrics


def fix_metadata(args):
    import numpy as np
    import pandas as pd
    metadata = pd.read_csv(args.step3_save_path / "metadata_of_features.csv")
    ##############################################################################################################
    # fix the DMSO Inner dosage for Mike Bolt Flav-Screen
    # TODO: Fix it using the plate-map itself and save/overwrite the fixed platemap,
    #  for mike bolt flav-screen experiments
    for it in ["dmso", "dmso-inner", "dmso-outer", "outer", "media"]:
        if np.isin(it, metadata["treatment"].to_list()):
            metadata.loc[metadata["treatment"] == it, "dosage"] = 0
            print(it, np.unique(metadata.loc[metadata["treatment"] == it]["dosage"]))
    metadata.to_csv(args.step3_save_path / "metadata_of_features.csv", index=False, float_format="%.2f")
    metadata["exp-id"] = args.experiment
    metadata.to_csv(args.step3_save_path / "metadata_of_features.csv", index=False, float_format="%.2f")


def set_default_datasets_hyperparameters(args):
    ##############################################################################
    # intensity rescaling hyperparameters
    args.w1_intensity_bounds = (5, 99.95)
    args.w2_intensity_bounds = (5, 99.95)
    args.w3_intensity_bounds = (5, 99.95)
    args.w4_intensity_bounds = (5, 99.95)
    args.w5_intensity_bounds = (5, 99.95)
    ##########################################################################
    # background correction hyperparameters
    """Set args.bg_sub to True first if you decide to do background subtraction."""
    args.bg_sub = False
    args.w1_bg_rad = 50
    args.w2_bg_rad = 100
    args.w3_bg_rad = 50
    args.w4_bg_rad = 100
    args.w5_bg_rad = 100
    #######################################################################
    # image channels order/index during data acquisition set by the investigator/microscope
    args.nucleus_idx = 0
    args.cyto_idx = 1
    args.nucleoli_idx = 2
    args.actin_idx = 3
    args.mito_idx = 4
    #######################################################################
    # hyperparameters/constants used in Cellpaint Step 2
    args.step2_segmentation_algorithm = "w1=cellpose_w2=cellpose"
    args.cellpose_nucleus_diam = 100
    args.cellpose_cyto_diam = 100
    args.cellpose_batch_size = 64
    args.cellpose_model_type = "cyto2"
    args.w1_min_size = 600
    args.w2_min_size = 700
    args.w3_min_size = 40
    args.w5_min_size = 200
    #######################################################
    # hyperparameters/constants used in Cellpaint Step 3
    args.multi_nucleus_dist_thresh = 40
    args.min_nucleoli_size_multiplier = .005
    args.max_nucleoli_size_multiplier = .3
    args.nucleoli_bd_area_to_nucleoli_area_threshold = .2
    args.w3_local_rescale_intensity_ub = 99.2
    args.w5_local_rescale_intensity_ub = 99.9
    return args


def set_seema_datasets_hyperparameters(args):
    ##############################################################################
    # intensity rescaling hyperparameters
    args.w1_intensity_bounds = (0.1, 99.99)
    args.w2_intensity_bounds = (0.1, 99.99)
    args.w3_intensity_bounds = (0.1, 99.99)
    args.w4_intensity_bounds = (0.1, 99.99)
    args.w5_intensity_bounds = (0.1, 99.99)
    ##########################################################################
    # background correction hyperparameters
    """Set args.bg_sub to True first if you decide to do background subtraction."""
    args.bg_sub = False
    args.w1_bg_rad = 50
    args.w2_bg_rad = 100
    args.w3_bg_rad = 50
    args.w4_bg_rad = 100
    args.w5_bg_rad = 100
    #######################################################################
    # image channels order/index during data acquisition set by the investigator/microscope
    args.nucleus_idx = 0
    args.cyto_idx = 1
    args.nucleoli_idx = 2
    args.actin_idx = 3
    args.mito_idx = 4
    #######################################################################
    # hyperparameters/constants used in Cellpaint Step 2
    args.step2_segmentation_algorithm = "w1=pycle_w2=pycle"
    args.cellpose_nucleus_diam = 30
    args.cellpose_cyto_diam = 30
    args.cellpose_batch_size = 64
    args.cellpose_model_type = "cyto2"
    args.w1_min_size = 200
    args.w2_min_size = 300
    args.w3_min_size = 5
    args.w5_min_size = 30
    #######################################################
    # hyperparameters/constants used in Cellpaint Step 3
    args.multi_nucleus_dist_thresh = 20
    args.min_nucleoli_size_multiplier = .000001
    args.max_nucleoli_size_multiplier = .999
    args.nucleoli_bd_area_to_nucleoli_area_threshold = .01
    args.w3_local_rescale_intensity_ub = 99.99
    args.w5_local_rescale_intensity_ub = 99.99
    return args


def set_jump_consortium_datasets_cpg0012_hyperparameters(args):
    ##########################################################################
    # background correction hyperparameters
    """Set args.bg_sub to True first if you decide to do background subtraction."""
    args.bg_sub = False
    args.w1_bg_rad = 50
    args.w2_bg_rad = 100
    args.w3_bg_rad = 50
    args.w4_bg_rad = 100
    args.w5_bg_rad = 100
    #######################################################################
    # image channels order/index during data acquisition set by the investigator/microscope
    args.nucleus_idx = 0
    args.cyto_idx = 1
    args.nucleoli_idx = 2
    args.actin_idx = 3
    args.mito_idx = 4
    #######################################################################
    # hyperparameters/constants used in Cellpaint Step 2
    args.step2_segmentation_algorithm = "w1=cellpose_w2=cellpose"
    args.cellpose_nucleus_diam = 20
    args.cellpose_cyto_diam = 30
    args.cellpose_batch_size = 64
    args.cellpose_model_type = "cyto2"
    args.w1_min_size = 400
    args.w2_min_size = 500
    args.w3_min_size = 4
    args.w5_min_size = 30
    #######################################################
    # hyperparameters/constants used in Cellpaint Step 3
    args.multi_nucleus_dist_thresh = 10
    args.min_nucleoli_size_multiplier = .000001
    args.max_nucleoli_size_multiplier = .999
    args.nucleoli_bd_area_to_nucleoli_area_threshold = .01
    args.w3_local_rescale_intensity_ub = 99.99
    args.w5_local_rescale_intensity_ub = 99.99
    args.min_nucleoli_size_multiplier = .000001
    args.max_nucleoli_size_multiplier = .999
    # args.nucleus_area_to_cyto_area_thresh = .6  this param is no longer available!!!
    return args


def set_jump_consortium_datasets_cpg0001_hyperparameters(args):
    ##########################################################################
    # background correction hyperparameters
    """Set args.bg_sub to True first if you decide to do background subtraction."""
    args.bg_sub = False
    args.w1_bg_rad = 50
    args.w2_bg_rad = 100
    args.w3_bg_rad = 50
    args.w4_bg_rad = 100
    args.w5_bg_rad = 100
    ############################################################
    # image channels order
    args.nucleus_idx = 4
    args.cyto_idx = 3
    args.nucleoli_idx = 2
    args.actin_idx = 1
    args.mito_idx = 0
    #######################################################################
    # hyperparameters/constants used in Cellpaint Step 2
    args.step2_segmentation_algorithm = "w1=cellpose_w2=cellpose"
    args.cellpose_nucleus_diam = 20
    args.cellpose_cyto_diam = 25
    args.cellpose_batch_size = 64
    args.cellpose_model_type = "cyto2"
    args.w1_min_size = 400
    args.w2_min_size = 500
    args.w3_min_size = 4
    args.w5_min_size = 30
    ###########################################################################
    # hyperparameters/constants used in Cellpaint Step 3
    args.multi_nucleus_dist_thresh = 10
    args.min_nucleoli_size_multiplier = .000001
    args.max_nucleoli_size_multiplier = .999
    args.nucleoli_bd_area_to_nucleoli_area_threshold = .01
    args.w3_local_rescale_intensity_ub = 99.99
    args.w5_local_rescale_intensity_ub = 99.99
    args.min_nucleoli_size_multiplier = .000001
    args.max_nucleoli_size_multiplier = .999
    # args.nucleus_area_to_cyto_area_thresh = .6  this param is no longer available!!!
    return args


def main_worker(args):
    """
    This program has three modes:
        Always run main_worker using args.mode == "preview" first.

    1) args.mode="preview":
        It allows the user to see the result of segmentation
        quickly on a few set of images. This way they can make
        sure the hyperparameters of the program are chosen appropriately.

    2) args.mode="test":
        For developer only, Only if you would like to change the internals of the program
        It helps with debugging and making sure the logic of the code follows.
        It does not use the multiprocessing module in for loop.

    3) args.mode="full":
         Runs the main_worker on the entire set of tiff images in the
         args.main_path / args.experiment / args.img_folder folder.
         It uses the multiprocessing module in step 3 and 4 for speed-up.
    """
    if args.mode == "preview":
        preview_run_loop(args, num_wells=2, sample_wellids=None)
    else:
        # segmentation of nucleus and cytoplasm
        step2_main_run_loop(args)
        # matching nucleus and cytoplasm labels,
        # and segmenting nucleoli and mitochondria
        step3_main_run_loop(args)
        # generates feature matrices as csv files
        step4_main_run_loop(args)
        # generates DistanceMaps as xlsx files
        step5 = WellAggFeatureDistanceMetrics(args)
        step5.step5_main_run_loop()


if __name__ == "__main__":
    camii_server_flav = r"P:\tmp\MBolt\Cellpainting\Cellpainting-Flavonoid"
    camii_server_seema = r"P:\tmp\MBolt\Cellpainting\Cellpainting-Seema"
    camii_server_jump_cpg0012 = r"P:\tmp\Kazem\Jump_Consortium_Datasets_cpg0012"
    camii_server_jump_cpg0001 = r"P:\tmp\Kazem\Jump_Consortium_Datasets_cpg0001"
    kazem_pc_ext_drive = "F:\\Cellpainting"
    pairs = \
        [
            # ######## ("20220607-CP-FStossi-Density-BM-U20S", kazem_pc_ext_drive),
            # ####### ("20220817-CP-FStossi-Density-BM_20220817_120119", "I:\\Cellpainting"),
            # ###### ####### ########### ("20220831-CP-FStossi-DRC-BM-R01_20220831_173200", "G:\\Cellpainting"),

            ##############################################################
            # ("20220831-CP-FStossi-DRC-BM-R01_20220831_173200", kazem_pc_ext_drive),
            # ("20220908-CP-FStossi-DRC-BM-R02-20220908_142836", kazem_pc_ext_drive),

            # ("20221102-CP-FStossi-DRC-BM-celllines-P01_20221102_144836", kazem_pc_ext_drive),
            # ("20221102-CP-FStossi-DRC-BM-celllines-P02_20221103_143400", kazem_pc_ext_drive),
            #
            # ("20221109-CP-FStossi-DRC-BM-P01", kazem_pc_ext_drive),
            # ("20221109-CP-FStossi-DRC-BM-P02", kazem_pc_ext_drive),
            #
            # ("20221116-CP-FStossi-DRC-BM-P01", kazem_pc_ext_drive),
            # ("20221116-CP-FStossi-DRC-BM-P02", kazem_pc_ext_drive),
            #
            # ("20230111-CP-FStossi-compoundscelllines-P01", kazem_pc_ext_drive),
            # ("20230111-CP-FStossi-compoundscelllines-P02", kazem_pc_ext_drive),
            #
            # ("20230119-CP-FStossi-QCcelllines-EXP01", kazem_pc_ext_drive),
            # ("20230124-CP-FStossi-QCcelllines-EXP02", kazem_pc_ext_drive),
            ####################################################################
            # ("20230112-CP-MBolt-Seema", camii_server_seema),
            # ("20230116-CP-MBolt-Seema", camii_server_seema),
            # ("20230120-CP-MBolt-Seema", camii_server_seema),
            # ("20230124-CP-MBolt-Seema", camii_server_seema),
            # ("20230210-CP-MBolt-Seema_100617", camii_server_seema),   # ran out of memory
            # ("20230127-CP-MBolt-Seema_20230127_152035", camii_server_seema),
            # ("20230203-CP-MBolt-Seema_20230203_174509", camii_server_seema),
            # ("20230216-CP-MBolt-Seema_20230223_091810", camii_server_seema),
            # ("20230511-CP-MBolt-Seema-HT29ShScr_20230511_171732", camii_server_seema),
            ("20230616-CP-Enteroids-Seema_20230616_162124", camii_server_seema),
            ########################################################################
            # # ##### on F drive
            # # # ###### Mike Bolt Bladder Cell-lines ######
            # ("20230119-CP-MBolt-Bladder", kazem_pc_ext_drive),
            # ("20230203-CP-MBolt-Bladder_20230202_131118", kazem_pc_ext_drive),
            # # ###########################################################################
            # # # ###### Mike Bolt FlavScreen ######
            # ("20230218-CP-MBolt-FlavScreen-5637_20230222_154337", camii_server_flav),
            # # ("20230219-CP-MBolt-FlavScreen-UMUC3_20230222_092057", camii_server_flav),  # bad plate, get rid
            # ("20230221-CP-MBolt-FlavScreen-RT4_20230227_111543", camii_server_flav),
            # ("20230223-CP-MBolt-FlavScreen-5637_20230227_163911", camii_server_flav),
            # ("20230224-CP-MBolt-FlavScreen-RT4_20230228_130627", camii_server_flav),
            # ("20230228-CP-MBolt-FlavScreen-5637_20230302_170729", camii_server_flav),
            # ("20230229-CP-MBolt-FlavScreen-RT4_20230303_103000", camii_server_flav),
            # ("20230302-CP-MBolt-FlavScreen-5637-Rerun_20230309_170739", camii_server_flav),

            # # ("20230303-CP-MBolt-FlavScreen-RT4_20230308_102430", camii_server_flav),  # bad images
            # ("20230314-CP-MBolt-FlavScreen-UMUC3_20230314_164600", camii_server_flav),
            # ("20230315-CP-MBolt-FlavScreen-UMUC3_20230315_111942", camii_server_flav),
            # ("20230316-CP-MBolt-FlavScreen-UMUC3-1-2_20230316_155210", camii_server_flav),
            # ("20230317-CP-MBolt-FlavScreen-UMUC3-2-2_20230317_091741", camii_server_flav),

            # ("20230407-CP-MBolt-FlavScreen-5637-Ub1-3_20230407_105529", camii_server_flav),
            # ("20230408-CP-MBolt-FlavScreen-5637-Ub2-3_20230407_165239", camii_server_flav),
            #
            # ("20230411-CP-MBolt-FlavScreen-UMUC3-1-3_20230412_190700", camii_server_flav),
            # ("20230412-CP-MBolt-FlavScreen-UMUC3-2-3_20230413_002234", camii_server_flav),
            #
            # # ("20230413-CP-MBolt-FlavScreen-RT4-1-3_20230415_005621", camii_server_flav),  # weird plates
            # # ("20230414-CP-MBolt-FlavScreen-RT4-2-3_20230414_194408", camii_server_flav),  # weird plates
            #
            # ("20230420-CP-MBolt-FlavScreen-5637-RT4-UMUC3_20230424_123359", camii_server_flav),
            # ("20230427-CP-MBolt-FlavScreen-RT4-5637-UMUC3_20230428_151300", camii_server_flav),
            #
            # ("20230518-CP-MBolt-FlavScrPt1-RT4_20230521_050728", camii_server_flav),
            # ("20230519-CP-MBolt-FlavScrPt2-RT4_20230521_093423", camii_server_flav),
            #######################################################################################

            ########################################################################
            # # ##### on P Cluster: dataset from jump consortium cpg0012
            # ("24278", camii_server_jump_cpg0012),
            # ("24279", camii_server_jump_cpg0012),
            # ("24280", camii_server_jump_cpg0012),
            # ("24293", camii_server_jump_cpg0012),
            # ("26224", camii_server_jump_cpg0012),
            # ("26232", camii_server_jump_cpg0012),
            # ("26239", camii_server_jump_cpg0012),
            # ("26247", camii_server_jump_cpg0012),
            #
            # ("24305", camii_server_jump_cpg0012),
            # ("24306", camii_server_jump_cpg0012),
            # ("24307", camii_server_jump_cpg0012),
            # ("24352", camii_server_jump_cpg0012),
            # ("25955", camii_server_jump_cpg0012),
            # ("25962", camii_server_jump_cpg0012),
            # ("25965", camii_server_jump_cpg0012),
            # ("25966", camii_server_jump_cpg0012),
            #
            # ("24310", camii_server_jump_cpg0012),
            # ("24311", camii_server_jump_cpg0012),
            # ("24312", camii_server_jump_cpg0012),
            # ("24313", camii_server_jump_cpg0012),
            # ("25985", camii_server_jump_cpg0012),
            # ("25986", camii_server_jump_cpg0012),
            # ("25987", camii_server_jump_cpg0012),
            # ("25988", camii_server_jump_cpg0012),

            ########################################################################
            # # ##### on P Cluster: dataset from jump consortium cpg0001

            # ("BR00121431", camii_server_jump_cpg0001),
            # ("BR00121432", camii_server_jump_cpg0001),
            # ("BR00121433", camii_server_jump_cpg0001),
            # ("BR00121434", camii_server_jump_cpg0001),
            # ("BR00121435", camii_server_jump_cpg0001),
            # ("BR00121440", camii_server_jump_cpg0001),

        ]
    for exp_fold, main_path in pairs:
        # entry point of the program is creating the necessary args
        print("*********************************************************"
              "*********************************************************"
              "*********************************************************"
              "*********************************************************")
        print(exp_fold, main_path)
        start_time = time.time()
        args = Args(experiment=exp_fold, main_path=main_path, mode="full").args
        # args = set_default_datasets_hyperparameters(args)
        args = set_seema_datasets_hyperparameters(args)
        main_worker(args)
        print(f"program finished analyzing experiment   "
              f"{args.experiment} in {(time.time()-start_time)/3600} hours ... ")
        print("*********************************************************"
              "*********************************************************"
              "*********************************************************"
              "*********************************************************")
