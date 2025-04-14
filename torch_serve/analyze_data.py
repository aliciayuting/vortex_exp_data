import os
import csv
import glob
import numpy as np

# ------------------------------------------
# Config
# ------------------------------------------
BASE_DIR = "."  # directory containing n0/, n1/, ...
LOG_FILENAME = "inference_times.csv"
WARMUP_SKIP = 100


# ------------------------------------------
# Utils
# ------------------------------------------
def parse_log_file(filepath, skip=WARMUP_SKIP):
    records = []

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append((
                float(row["start_time"]),
                float(row["end_time"]),
                float(row["latency_sec"]),
            ))

    # Drop first N records
    if len(records) <= skip:
        return [], [], []

    trimmed = records[skip:]
    start_times = [r[0] for r in trimmed]
    end_times   = [r[1] for r in trimmed]
    durations   = [r[2] for r in trimmed]

    return start_times, end_times, durations


def compute_throughput(start_times, end_times):
    if not start_times or not end_times:
        return 0.0
    time_span = max(end_times) - min(start_times)
    if time_span <= 0:
        return 0.0
    return len(end_times) / time_span


def compute_latency_stats(durations):
    durations = np.array(durations)
    return {
        "count": len(durations),
        "mean": np.mean(durations),
        "p50": np.percentile(durations, 50),
        "p90": np.percentile(durations, 90),
        "p99": np.percentile(durations, 99),
    }


# ------------------------------------------
# Main
# ------------------------------------------
def main():
    node_dirs = sorted(glob.glob(os.path.join(BASE_DIR, "n*/")))
    if not node_dirs:
        print("No node directories found.")
        return

    all_durations = []
    all_start_times = []
    all_end_times = []

    print("\n Per-node Metrics:\n" + "-" * 30)
    for node_dir in node_dirs:
        node_name = os.path.basename(os.path.normpath(node_dir))
        log_path = os.path.join(node_dir, LOG_FILENAME)

        if not os.path.exists(log_path):
            print(f"[{node_name}] Log file not found.")
            continue

        starts, ends, durs = parse_log_file(log_path)
        if not durs:
            print(f"[{node_name}] Not enough data after warm-up.")
            continue

        latency = compute_latency_stats(durs)
        throughput = compute_throughput(starts, ends)

        all_durations.extend(durs)
        all_start_times.extend(starts)
        all_end_times.extend(ends)

        print(f"[{node_name}]")
        print(f"  Requests       : {latency['count']}")
        print(f"  Throughput     : {throughput:.2f} req/s")
        print(f"  Latency (s)    : mean={latency['mean']:.4f}, p50={latency['p50']:.4f}, p90={latency['p90']:.4f}, p99={latency['p99']:.4f}")

    # Aggregate stats
    print("\n Aggregate Metrics:\n" + "-" * 30)
    if all_durations:
        latency = compute_latency_stats(all_durations)
        throughput = compute_throughput(all_start_times, all_end_times)
        print(f"Total Requests    : {latency['count']}")
        print(f"Overall Throughput: {throughput:.2f} req/s")
        print(f"Latency (s)       : mean={latency['mean']:.4f}, p50={latency['p50']:.4f}, p90={latency['p90']:.4f}, p99={latency['p99']:.4f}")
    else:
        print("No data collected after warm-up.")

if __name__ == "__main__":
    main()