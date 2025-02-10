## `generate_box_plot` usage

* Provide data file directory and output directory as first and second command line arguments, respectively
* Expects `data.json` file in current directory
* `data.json` should list all segments to generate box plots for

**Example:**
```data.json
{
    "drop": 3, // specify how many samples from the top to drop
    "segments": [
        {
            "file_name": "step_A_transfer_to_gpu.csv", // data file name
            "name": "Step A Transfer to GPU", // plot title
            "type": "horizontal_csv" // headerless CSV, all trials in 1 row
        },
        {
            "file_name": "step_C_transfer_time_100_times.csv",
            "type": "csv", // CSV with header, trials along columns
            "columns": [ // 1 entry per column to plot
                {
                    "name": "Step C Data Transfer Time", // plot title
                    "csv_name": "data_transfer_time(ns)", // column name used in CSV
                    "out": "step_C_data_transfer_time_box_plot.png" // optional output file name
                },
                {
                    "name": "Step C Output Transfer Time",
                    "csv_name": "output_transfer_time(ns)",
                    "out": "step_C_output_transfer_time_box_plot.png"
                }
            ]
        }
    ]
}
```

## `generate_bar_plot` usage

* Provide data file directory and output directory as first and second command line arguments, respectively
* Expects `data.json` file in current directory
* `data.json` should list all bars in order

**Example:**
```data.json
{
    "drop": 3, // specify how many samples from the top to drop
    "bars": [
        {
            "name": "Step A", // bar x-axis label
            "data": [ // specify segments within each bar
                {
                    "file_name": "step_A_transfer_to_gpu.csv",
                    "bar_group": "Transfer to GPU", // bar segment group name
                    "type": "horizontal_csv"
                },
                {
                    "file_name": "step_A_runtime.csv",
                    "bar_group": "Model runtime", // different group = different color but same bar
                    "type": "horizontal_csv"
                }
            ]
        },
        {
            "name": "Step C",
            "data": [
                {
                    "file_name": "step_C_latency_100_times.csv",
                    "type": "csv",
                    "columns": [
                        { // each column is treated as a new segment
                            "csv_name": "model_run_time(ns)",
                            "bar_group": "Model runtime"
                        }
                    ]
                }
            ]
        }
    ]
}
```
