import os, sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
import AI4GSD

## Demo of code.
if __name__ == "__main__":
    #%% Define working folder.
    WorkDir = r'/home/chen200/F/VisionAI2'
    folders = ['NvidiaH100_NoCut_12Filter',
               'NvidiaH100_NoCut_12Filter_Run2',
               'NvidiaH100_NoCut_12Filter_Run3',
               'NvidiaH100_0.1Cut_12Filter',
               'NvidiaH100_NoCut_12Filter_SingleDiameter']
    
    #%% Call functions.   
    overwrite= True
    device='0'
    for folder in folders:
        DataDir = os.path.join(WorkDir,folder)
        subfolders = AI4GSD.getFolders(DataDir)
        print(f'Master folder: {folder}')
        for folder in subfolders:
            img_size = 1280
            PhotoDir = DataDir + os.sep + folder                               # Where you save your photos.
            sts = AI4GSD.yolov5_predict(
                img_dir=PhotoDir,
                img_size = img_size,
                overwrite=overwrite,
                device=device,
                save_overlay=False,
                write_time_only=True,
                )
            
    #%% End.
