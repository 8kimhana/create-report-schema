# Report Schema Tool
This tool is used to create report schemas for new dwh datasources.
It uses python3 so make sure if you want to use this tool you have any version of python 3.XX installed

## How to use

1. First you must clone this repo locally 
2. Then you can cd into the directory
3. Make sure you have the dimensions and metrics sperated into different .txt or .csv files
###### If using .csv files make sure you have AT LEAST id, name, and description columns
###### If using .txt files all you need is the id/name and you can format the rest later
4. Run this command in the directory
```
python3 create-schema.py
```
5. Follow the prompts and windows
6. Copy and paste the output to your report file in your datasource
7. Viola
