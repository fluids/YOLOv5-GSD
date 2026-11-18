# YOLOv5 for Stream Grain Detection and Runtime Benchmark

This repository provides Python scripts and Jupyter notebooks for detecting streambed sediment grains using the pretrained **M0c YOLOv5 model** described in [Chen et al. (2024)](https://doi.org/10.1029/2023WR036456). 

It supports inference on CPUs and NVIDIA GPUs, saves grain bounding boxes and optional annotated images, and records per-image processing times. The demos were developed and tested on an Intel Core i9 CPU in a [Dell Precision 5820 Tower Workstation](https://www.dell.com/en-us/shop/desktop-computers/spd/precision-5820-workstation) and an NVIDIA H100 GPU on PNNL’s Marianas high-performance computing (HPC) system. Other CPUs and compatible NVIDIA GPUs can be used with an appropriate PyTorch installation. 

Converting the detected bounding boxes to physical grain sizes and calculating grain-size distributions require pixel size information and additional processing. [AI4GSD](https://github.com/pnnl/AI4GSD) provides these capabilities, including automated pixel size estimation through Scale AI.

## Repository Contents

| Path | Description |
| --- | --- |
| [Demo_JupyterNotebook](Demo_JupyterNotebook) | Four interactive notebooks for grain detection and processing-time measurements on CPUs and GPUs. |
| [Demo_Python_Release](Demo_Python_Release) | Python script equivalents of the four notebooks. |
| [AI4GSD](src/AI4GSD) | Supporting functions, including `yolov5_predict()`, and utilities adapted from [AI4GSD](https://github.com/pnnl/AI4GSD). |
| [yolov5](src/yolov5) | Ultralytics YOLOv5 source code with custom modifications. |
| [yolov5/models_trained/yolo_v5_best.pt](yolov5/models_trained/yolo_v5_best.pt) | Pretrained M0c model weights described in [Chen et al. (2024)](https://doi.org/10.1029/2023WR036456). |
| [Install_Linux.md](Install_Linux.md) | Installation instructions for CPU use on Ubuntu 20.04 and GPU use on Rocky Linux 9.5. |
| [Install_Windows.md](Install_Windows.md) | Installation instructions for CPU use on Windows. |

## Installation

For Ubuntu or HPC systems, please follow [Install_Linux.md](Install_Linux.md) to create the environment for your hardware. 

For Windows, please follow [Install_Windows.md](Install_Windows.md) to create the environment for your hardware. 

## Download the Example Data

Download the benchmark data from [ESS-DIVE, DOI: 10.15485/2588483](https://doi.org/10.15485/2588483). The image data must be obtained separately from the code archive.

| Demo hardware | Download files beginning with | Example master folder |
| --- | --- | --- |
| NVIDIA GPU | `NvidiaH100_` | `NvidiaH100_NoCut_12Filter` |
| CPU | `IntelCoreI9_` | `IntelCoreI9_NoCut_12Filter` |

Extract the files into a common data directory. Set `WorkDir` to that directory, with the master folders immediately beneath it. Each master folder contains image-set subfolders, and the images are read directly from those subfolders. For example:

```text
D:/Data/VisionAI/NvidiaH100_NoCut_12Filter/20260430_YC_YRBCRBWAUSA/<image files>
```

Here, `WorkDir` is `D:/Data/VisionAI`. Edit the demo's `folders` list to include only the master folders you downloaded. The GPU demos list five master folders and the CPU demos list three; missing folders must be removed from the list or downloaded before running.

The beckmar data contains the following images and their sources:

| Image set | Contents | Source |
| --- | --- | --- |
| `20260430_YC_YRBCRBWAUSA` | 10 smartphone photos and 9 drone images | Chen et al. (2024) and the [ESS-DIVE dataset](https://doi.org/10.15485/2588483). |
| `20260430_MairD2026IG2_*` | 35 images across the image-set folders | [ImageGrains 2.0 dataset, v2](https://doi.org/10.5281/zenodo.17866827). |
| `20250916_DetertM2012_FieldValidateBaseGrain` | 1 validation image | [BASEGRAIN](https://basement.ethz.ch/download/tools/basegrain.html). |
| `20250916_MairD2024_FieldValidateMair2024K1` | 1 validation image | [ImageGrains dataset and model weights, v1](https://doi.org/10.5281/zenodo.8005771). |

## Run the Jupyter Notebook Demos

From the outer project directory, activate the environment and launch Jupyter inside the notebook folder:

```bash
conda activate yolov5
cd Demo_JupyterNotebook
python -m notebook
```

Select **Python (yolov5)** as the kernel, open a demo below, update its configuration, and run the cells in order. Starting Jupyter in this folder matches the notebooks' `Path.cwd().parent` import setup.

| Demo | Purpose | Device |
| --- | --- | --- |
| [Demo 0: GPU Predictions](Demo_JupyterNotebook/Demo0_yolov5_predictions_H100.ipynb) | Save grain labels, annotated images, and timing CSVs. | NVIDIA GPU (`'0'`) |
| [Demo 1: CPU Predictions](Demo_JupyterNotebook/Demo1_yolov5_predictions_I9.ipynb) | Save grain labels, annotated images, and timing CSVs. | CPU (`'cpu'`) |
| [Demo 2: GPU Timing](Demo_JupyterNotebook/Demo2_yolov5_time_only_H100.ipynb) | Measure runtime without saving new labels or annotated images. | NVIDIA GPU (`'0'`) |
| [Demo 3: CPU Timing](Demo_JupyterNotebook/Demo3_yolov5_time_only_I9.ipynb) | Measure runtime without saving new labels or annotated images. | CPU (`'cpu'`) |

Before running, check:

- **`WorkDir`**: your extracted data directory, for example `Path('D:/Data/VisionAI')`.
- **`folders`**: the master folders to process.
- **`device`**: `'cpu'` for CPU inference or `'0'` for the first visible NVIDIA GPU.
- **`overwrite`**: all supplied demos default to `True`. See the output behavior below before rerunning them.
- **`save_overlay`**: set to `True` to save annotated images in prediction demos.

Prediction demos use `img_size=320` for image-set folder names containing `20260430_MairD2026IG2`, and `1280` otherwise. Timing demos use `1280` for every image set. Account for this difference when comparing runtimes.

Files ending in `_executed.ipynb` contain saved GPU example outputs.

## Run the Python Scripts

Open a script in [Demo_Python_Release](Demo_Python_Release), update `WorkDir`, `folders`, and the other settings, then run it from a terminal or an editor such as Spyder. From the outer project directory:

```bash
# GPU predictions
python Demo_Python_Release/Demo0_yolov5_predictions_H100.py

# CPU predictions
python Demo_Python_Release/Demo1_yolov5_predictions_I9.py

# GPU timing only
python Demo_Python_Release/Demo2_yolov5_time_only_H100.py

# CPU timing only
python Demo_Python_Release/Demo3_yolov5_time_only_I9.py
```

Choose the command for the task you want to run.


## Outputs and Timing

Each processed image-set folder receives:

| Output | Location relative to the image-set folder |
| --- | --- |
| Per-image timing CSV | `Time_V3_<folder>_YOLOv5.0.0.csv` |
| YOLO detection labels | `grains_predicts/<folder>_YOLOv5.0.0_35/labels/` |
| Annotated images, when enabled | `grains_predicts/<folder>_YOLOv5.0.0_35/` |

These paths assume the wrapper's default naming settings. Label rows contain `class x_center y_center width height confidence`, with box coordinates normalized by image dimensions. Images without detections may have no label file.

The CSV records image and model identifiers, original image dimensions, image-reading time, preprocessing time, inference time, postprocessing time (non-maximum suppression), and total time, in seconds. `Predict_time_seconds` and `Total_time_seconds` currently contain the same total: image reading plus preprocessing, inference, and postprocessing. It excludes model loading, process startup, and writing overlays or labels. The printed folder processing time includes broader wrapper overhead and should not be compared directly with per-image CSV totals.

## Citation and Acknowledgments

Please cite the model paper and the relevant image datasets when reusing these materials:

Chen, Y., et al. (2024). Quantifying streambed grain size, uncertainty, and hydrobiogeochemical parameters using machine learning model YOLO. *Water Resources Research*, 60, e2023WR036456. https://doi.org/10.1029/2023WR036456

The demo notebooks provide additional source references. This project incorporates [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5); its bundled license is available in [src/yolov5/LICENSE](src/yolov5/LICENSE). Local helper source headers contain additional usage and license statements; contact the author for clarification of terms covering those files.

## Contact

Yunxiang Chen, Pacific Northwest National Laboratory, Richland, WA, USA. 
Email: [yunxiang.chen@pnnl.gov](mailto:yunxiang.chen@pnnl.gov)
