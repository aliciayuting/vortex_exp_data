#!/bin/bash

# GPU memory log file
FINAL_GPU_LOG="memgpu_log.dat"
TEMP_GPU_FILE=$(mktemp)

# DCGM log file
DCGM_LOG="dcgm_log.dat"

# Monitoring intervals
MEMORY_INTERVAL=5  # seconds
DCGM_INTERVAL=1  # seconds

# Compute DCGM sampling interval in milliseconds
DCGM_SAMPLING_INTERVAL=$((DCGM_INTERVAL * 1000))

# Write header for GPU memory log
echo "Timestamp, GPU_ID, Total_Memory_MB, Used_Memory_MB, Free_Memory_MB" > "$TEMP_GPU_FILE"

# Start DCGM monitoring in the background
echo "Starting DCGM monitoring (logs to $DCGM_LOG)..."
dcgmi dmon -e 203,204,1001,1002,1003,1004,1005,1007,155 -d "$DCGM_SAMPLING_INTERVAL" > "$DCGM_LOG" &

# Get DCGM process ID (to stop later)
DCGM_PID=$!

# Function to handle script termination (Ctrl+C)
cleanup() {
    echo "Stopping DCGM monitoring..."
    kill "$DCGM_PID"

    echo "Saving collected GPU memory usage to $FINAL_GPU_LOG..."
    mv "$TEMP_GPU_FILE" "$FINAL_GPU_LOG"

    echo "Logs saved to $FINAL_GPU_LOG and $DCGM_LOG."
    exit 0
}

# Trap Ctrl+C (SIGINT) to call cleanup function
trap cleanup SIGINT

echo "Logging GPU memory usage every $MEMORY_INTERVAL seconds. DCGM monitoring every $DCGM_INTERVAL second."
echo "Press Ctrl+C to stop and save logs."

while true; do
    # Get the current timestamp
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

    # Extract GPU memory usage using nvidia-smi
    nvidia-smi --query-gpu=index,memory.total,memory.used,memory.free --format=csv,noheader,nounits | while IFS=',' read -r GPU_ID TOTAL USED FREE; do
        echo "$TIMESTAMP, $GPU_ID, $TOTAL, $USED, $FREE" >> "$TEMP_GPU_FILE"
    done

    # Wait before the next measurement
    sleep $MEMORY_INTERVAL
done
