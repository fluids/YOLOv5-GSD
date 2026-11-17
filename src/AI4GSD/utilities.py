import os, sys, pathlib, subprocess, shutil, time, re
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from urllib.request import urlopen

#%% Downloading the pre-trained model if not found in desired folder.
def get_model(model_dir, model_url):
    """Download a missing model and return its local path."""
    model_dir = Path(model_dir)
    
    if model_dir.is_file() and model_dir.stat().st_size > 0: return model_dir
    
    model_dir.parent.mkdir(parents=True, exist_ok=True)
    temp_path = model_dir.with_suffix(model_dir.suffix + ".part")

    with urlopen(model_url, timeout=60) as response, temp_path.open("wb") as f:
        total = int(response.headers.get("Content-Length", 0)) or None

        with tqdm(total=total, unit="B", unit_scale=True,
                  desc=f"Downloading {model_dir.name}") as bar:
            while chunk := response.read(1024 * 1024):
                f.write(chunk)
                bar.update(len(chunk))

            if bar.n == 0 or (total is not None and bar.n != total):
                raise IOError(f"Download empty or incomplete: {model_dir}")

    temp_path.replace(model_dir)

    if not model_dir.is_file() or model_dir.stat().st_size != bar.n:
        raise IOError(f"Model was not successfully saved to: {model_dir}")

    print(f"Model saved to: {model_dir}")
    return model_dir

#%% Loading a pre-trained YOLOv5 model to predict and output time.
def yolov5_predict(img_dir,img_size=1280,conf=0.35,device='cpu',
                      save_overlay=False, model_name='YOLOv5.0.0',
                      hide_conf = True, save_folder='grains_predicts',
                      foldername_save=None,line_thickness=2,overwrite=False,
                      max_det=10000,hide_class=True,write_time_only=False):
    
    ts1 = time.time()
    foldername = os.path.basename(img_dir)
    model_name += ".0.0" if len(model_name.split('.')) == 1 else ""
    if foldername_save is None:
        foldername_save = foldername + '_' + model_name + '_' + "{:.0f}".format(conf*100)
    output_dir = os.path.join(img_dir, save_folder, foldername_save)
    label_dir = os.path.join(output_dir, "labels")
    
    CodeDir = str(pathlib.Path(__file__).resolve().parents[1])
    src_dir = os.path.join(CodeDir,'yolov5')
    model_dir = os.path.join(src_dir,"models_trained","yolo_v5_best.pt")
    model_url = "https://media.githubusercontent.com/media/fluids/models/main/YOLOv5-GSD/yolo_v5_best.pt"
    get_model(model_dir,model_url)
    
    csvname = 'Time_V3_' + foldername + '_' + model_name + '.csv'
    csvpath = os.path.join(img_dir,csvname)
    colnames = ['Name', 'Folder', 'Model_ID', 'Model_File', 'Width_pixel',
                'Height_pixel', 'Imagereading_time_seconds', 'Predict_time_seconds',
                'Preprocess_time_seconds', 'Inference_time_seconds',
                'Postprocess_time_seconds', 'Total_time_seconds']
    
    # Checking if exists and overwrite.
    if os.path.exists(label_dir) and os.path.isfile(csvpath) and not overwrite:
        print('Founding existing labels, skipping...')
        sts_df = pd.read_csv(csvpath)
    else:
        if os.path.exists(label_dir): shutil.rmtree(label_dir)                 # Remove existing labels.
        cmd = [
            sys.executable,
            os.path.join(src_dir, "detect_timeinfo.py"),
            "--weights", model_dir,
            "--source", img_dir,
            "--img", str(img_size),
            "--save-txt",         
            "--save-conf",   
            "--device", device,
            "--conf", str(0.25),
            "--max-det", str(max_det),
            "--project", os.path.join(img_dir, save_folder),
            "--name", foldername_save,
            "--line-thickness", str(line_thickness),
            "--exist-ok"
        ]
        # Option 2 only write time, but not save any results.
        cmd2 = [
            sys.executable,
            os.path.join(src_dir, "detect_timeinfo.py"),
            "--weights", model_dir,
            "--source", img_dir,
            "--img", str(img_size),
            "--device", device,
            "--conf", str(0.25),
            "--max-det", str(max_det),
            "--project", os.path.join(img_dir, save_folder),
            "--name", foldername_save,
            "--line-thickness", str(line_thickness),
            "--exist-ok",
            "--nosave",                                                        # Do not save prediction images
        ]
        if write_time_only: cmd = cmd2
        
        if not save_overlay: cmd.append("--nosave")
        if hide_conf: cmd.append("--hide-conf")
        if hide_class: cmd.append("--hide-labels")
        
        result = subprocess.run(cmd,check=True,text=True,capture_output=True)
        
        # Parsing data.
        log_text = result.stdout + result.stderr
        pattern = (
            r"image\s+\d+/\d+\s+(.+?):.*?"
            r"raw\s+(\d+)x(\d+),\s+"
            r"load\s+([\d.]+)ms,\s+"
            r"pre\s+([\d.]+)ms,\s+"
            r"infer\s+([\d.]+)ms,\s+"
            r"NMS\s+([\d.]+)ms,\s+"
            r"total\s+([\d.]+)ms"
        )
        matches = re.findall(pattern, log_text)
        sts = []
        for fname, raw_w, raw_h, tload, tpre, tinf, tpos, ttotal in matches:
            sts.append([
                os.path.basename(fname),
                foldername,
                model_name,
                os.path.basename(model_dir),
                int(raw_w),
                int(raw_h),
                float(tload) / 1000,
                float(ttotal) / 1000,
                float(tpre) / 1000,
                float(tinf) / 1000,
                float(tpos) / 1000,
                float(ttotal) / 1000
            ])
        sts_df = pd.DataFrame(sts, columns=colnames)
        if os.path.isfile(csvpath): os.remove(csvpath)
        sts_df.to_csv(csvpath, index=False)  
        
    ts1 = time.time() - ts1
    print(f"Processing {foldername} in {ts1:.2f} seconds")
    
    return sts_df

#%%