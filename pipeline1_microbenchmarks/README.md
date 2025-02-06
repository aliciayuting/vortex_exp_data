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
