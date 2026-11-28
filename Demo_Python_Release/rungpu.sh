#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

if command -v conda >/dev/null 2>&1; then
  eval "$(conda shell.bash hook)"
  conda activate yolov5
else
  echo "ERROR: conda is not available."
  exit 1
fi

RUN_LOG="rungpu.log"
rm -f "${RUN_LOG}"
exec > >(tee "${RUN_LOG}") 2>&1

echo "============================================================"
echo "Environment information"
echo "============================================================"
echo "Conda environment: ${CONDA_DEFAULT_ENV:-yolov5}"
echo "CONDA_PREFIX: ${CONDA_PREFIX:-none}"
echo "Running on host: $(hostname)"
echo "SLURM_JOB_ID: ${SLURM_JOB_ID:-none}"
echo "SLURM_NODELIST: ${SLURM_NODELIST:-none}"
"${CONDA_PREFIX}/bin/python" -c 'import sys; print("Python executable:", sys.executable)' 

scripts=(
  "Demo0_yolov5_predictions_H100.py"
  "Demo2_yolov5_time_only_H100.py"
)

echo "Starting all GPU demos at: $(date)"
echo "Number of demos: ${#scripts[@]}"

for ((taskid=0; taskid<${#scripts[@]}; taskid++)); do
  SCRIPT="${scripts[$taskid]}"
  LOGFILE="${SCRIPT%.py}.log"

  echo "============================================================"
  echo "GPU status"
  echo "============================================================"
  if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi -i 0 --query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu,pstate --format=csv
  else
    echo "nvidia-smi is not available."
  fi
  "${CONDA_PREFIX}/bin/python" -u -c 'import torch; print("CUDA available:", torch.cuda.is_available()); print("CUDA device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "none")' 2>&1

  echo "============================================================"
  echo "Task id: ${taskid}"
  echo "Script: ${SCRIPT}"
  echo "Log file: ${LOGFILE}"
  echo "Starting task ${taskid} at: $(date)"
  echo "============================================================"

  rm -f "${LOGFILE}"
  "${CONDA_PREFIX}/bin/python" -u "${SCRIPT}" 2>&1 | tee "${LOGFILE}"

  echo "Finished task id ${taskid} at: $(date)"
done

echo "============================================================"
echo "All GPU demos finished at: $(date)"
echo "============================================================"
