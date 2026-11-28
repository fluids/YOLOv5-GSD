import sys, os
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent / "src"))
import AI4GSD

## Demo of code.
if __name__ == "__main__":
    #%% Define working folder.
    WorkDir = r'/rcfs/projects/rcsfa/VisionAI'
    folders = ['NvidiaH100_NoCut_12Filter',
               'NvidiaH100_NoCut_12Filter_Run2',
               'NvidiaH100_NoCut_12Filter_Run3',
               'NvidiaH100_0.1Cut_12Filter',
               'NvidiaH100_NoCut_12Filter_SingleDiameter']
    
    #%% Call functions.
    keyword = '20260430_MairD2026IG2'
    overwrite= True
    save_overlay = True
    device='0'
    hide_conf =  True
    for folder in folders:
        DataDir = os.path.join(WorkDir,folder)
        subfolders = AI4GSD.getFolders(DataDir)
        print(f'Master folder: {folder}')
        for folder in subfolders:
            img_size = 1280
            line_thickness = 2
            if keyword.lower() in folder.lower():
                img_size = 320
                line_thickness = 2
            PhotoDir = DataDir + os.sep + folder                               # Where you save your photos.
            sts = AI4GSD.yolov5_predict(
                img_dir=PhotoDir,
                img_size = img_size,
                overwrite=overwrite,
                device=device,
                save_overlay=save_overlay,
                line_thickness = line_thickness,
                hide_conf=hide_conf,
                label_dir='BeforeThreshold',
                )
        print('')
            
    #%% End.
