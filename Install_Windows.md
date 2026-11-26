# YOLOv5 Installation Guide for Windows 11 — CPU

This guide installs the Python environment and packages required to run the YOLOv5 demos on a Windows 11 computer using a CPU.

Install [Git for Windows](https://git-scm.com/download/win) before cloning the repository. Model weights download automatically if they are missing locally, so Git LFS is not required. An internet connection is required for the initial model download.

## Step 0 · Install Anaconda

Skip this step if Anaconda is already installed.

1. Download the [Anaconda installer for Windows](https://repo.anaconda.com/archive/Anaconda3-2026.07-1-Windows-x86_64.exe).
2. Double-click the downloaded `.exe` file.
3. Click **Next**, review the license agreement, and click **I Agree**.
4. Select **Just Me** unless you need an installation for all users.
5. Choose the installation folder. The default location is usually suitable.
6. Keep the default advanced options. You do not need to add Anaconda to the system PATH.
7. Click **Install**, wait for installation to finish, and click **Finish**.

## Step 1 · Open Anaconda PowerShell Prompt

Search for **Anaconda PowerShell Prompt** in the Windows Start menu and open it. If it is unavailable, use **Anaconda Prompt** instead.

Run all subsequent commands in this prompt.

## Step 2 · Create a Python environment

```powershell
conda create -n yolov5 python=3.10 -y
```

## Step 3 · Activate the environment

```powershell
conda activate yolov5
```

Activate this environment whenever you open a new prompt to use YOLOv5.

## Step 4 · Install PyTorch for CPU

```powershell
python -m pip install torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cpu
```

## Step 5 · Download the source code and install dependencies

Navigate to the directory where you want to store the code. For example:

```powershell
cd "D:\"
```

Download the customized [YOLOv5-GSD repository](https://github.com/fluids/YOLOv5-GSD):

```powershell
git clone https://github.com/fluids/YOLOv5-GSD.git
cd YOLOv5-GSD
```

From the repository root, install the dependencies in `src/YOLOv5-GSD/requirements.txt`:

```powershell
python -m pip install -r src/yolov5/requirements.txt
```

If the repository is already downloaded, navigate directly to its root directory and run the dependency installation command.

## Step 6 · Install additional integration packages

```powershell
python -m pip install natsort pyproj
```

## Step 7 · Install Jupyter Notebook

Install Jupyter Notebook and register the environment as a notebook kernel:

```powershell
python -m pip install notebook ipykernel
python -m ipykernel install --user --name yolov5 --display-name "Python (yolov5)"
```

## Step 8 · Verify the installation

Check for dependency conflicts:

```powershell
python -m pip check
```

Print package versions and GPU availability:

```powershell
python -c "import torch, torchvision, cv2, numpy, pandas, matplotlib; print('PyTorch:', torch.__version__); print('torchvision:', torchvision.__version__); print('OpenCV:', cv2.__version__); print('NumPy:', numpy.__version__); print('pandas:', pandas.__version__); print('Matplotlib:', matplotlib.__version__); print('CUDA available:', torch.cuda.is_available())"
```

For this CPU installation, `CUDA available: False` is expected.

After verification succeeds, see [Run the Jupyter Notebook Demos](README.md#run-the-jupyter-notebook-demos) or [Run the Python Scripts](README.md#run-the-python-scripts) for instructions on running the demos.
