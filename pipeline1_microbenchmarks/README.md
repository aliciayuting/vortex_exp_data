## Generating CDF, Histogram, & Box Plots

`python3 generate_plot.py INPUT_FILE_NAME [-p hist | cdf | box] [-o OUTPUT_FILE_NAME] [-r CSV_ROW_NAME] [-d DROP_COUNT] [-t TITLE]`

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
