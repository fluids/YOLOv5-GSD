# YOLOv5 Installation Guide for Linux

This guide provides CPU and GPU installation options using the following example systems:

- **Option A:** Intel Core i9 CPU on Ubuntu 20.04.
- **Option B:** NVIDIA H100 GPU on Rocky Linux 9.5.

Other Linux systems may require adjustments to package versions. Install Anaconda or Miniconda and Git before proceeding.

Model weights download automatically if they are missing locally. Git LFS is not required.

## Step 0: Open a terminal

Run all commands below in the terminal.

## Step 1: Create a Python environment

Choose one option based on your hardware.

### Option A: CPU — Example: Intel Core i9 on Ubuntu 20.04

```bash
conda create -n yolov5 python=3.8.13 -y
```

### Option B: GPU — Example: NVIDIA H100 on Rocky Linux 9.5

```bash
conda create -n yolov5 python=3.10 -y
```

## Step 2: Activate the environment

```bash
conda activate yolov5
```

Activate this environment whenever you open a new terminal to use YOLOv5.

## Step 3: Download the repository

Clone the customized [YOLOv5-GSD repository](https://github.com/fluids/YOLOv5-GSD):

```bash
git clone https://github.com/fluids/YOLOv5-GSD.git
cd YOLOv5-GSD
```

If you have already downloaded the repository, navigate to its root directory instead.

Run the remaining commands from this directory. The YOLOv5 source code and requirements file are located under `src/YOLOv5-GSD/`.

Pretrained model weights download automatically from [fluids/models](https://github.com/fluids/models) when needed. An internet connection is required for the initial download.

## Step 4: Install PyTorch

Choose the option corresponding to the environment created in Step 1.

### Option A: CPU — Example: Intel Core i9 on Ubuntu 20.04

```bash
python -m pip install torch==1.11.0+cpu torchvision==0.12.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu
```

### Option B: GPU — Example: NVIDIA H100 on Rocky Linux 9.5

Install the CUDA 11.8 build with a compatible NVIDIA driver:

```bash
python -m pip install torch==2.7.1 torchvision==0.22.1 torchaudio==2.7.1 --index-url https://download.pytorch.org/whl/cu118
```

## Step 5: Install YOLOv5 dependencies

From the repository root, run:

```bash
python -m pip install -r src/yolov5/requirements.txt
```

**Compatibility note:** The requirements file includes newer dependencies that may conflict with the older Python 3.8/PyTorch 1.11 CPU environment. Option A requires a separately tested requirements list. Installing dependencies may upgrade PyTorch; check the installed versions in Step 8.

## Step 6: Install additional integration packages

```bash
python -m pip install natsort pyproj
```

## Step 7: Install Jupyter Notebook

Install Jupyter Notebook and register the environment as a notebook kernel:

```bash
python -m pip install notebook ipykernel
python -m ipykernel install --user --name yolov5 --display-name "Python (yolov5)"
```

## Step 8: Verify the installation

Check for dependency conflicts:

```bash
python -m pip check
```

Print package versions and GPU availability:

```bash
python - <<'PY'
import torch
import torchvision
import cv2
import numpy
import pandas
import matplotlib

print("PyTorch:", torch.__version__)
print("torchvision:", torchvision.__version__)
print("OpenCV:", cv2.__version__)
print("NumPy:", numpy.__version__)
print("pandas:", pandas.__version__)
print("Matplotlib:", matplotlib.__version__)
print("CUDA available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
PY
```

For a CPU installation, `CUDA available: False` is expected. For a GPU installation, run this check on a GPU-equipped compute node and confirm that the GPU is detected.

See [Run the Jupyter Notebook Demos](README.md#run-the-jupyter-notebook-demos) or [Run the Python Scripts](README.md#run-the-python-scripts) for instructions on running the demos.
