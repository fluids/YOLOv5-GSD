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

RUN_LOG="runcpu.log"
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
  "Demo1_yolov5_predictions_I9.py"
  "Demo3_yolov5_time_only_I9.py"
)

echo "Starting all CPU demos at: $(date)"
echo "Number of demos: ${#scripts[@]}"

for ((taskid=0; taskid<${#scripts[@]}; taskid++)); do
  SCRIPT="${scripts[$taskid]}"
  LOGFILE="${SCRIPT%.py}.log"

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
echo "All CPU demos finished at: $(date)"
echo "============================================================"
