# decodelabs_tasks2
Analyze a dataset to understand patterns, trends, and distributions using Exploratory Data Analysis (EDA) techniques.

# Project-2: Exploratory Data Analysis (EDA)

## Goal

Analyze a dataset to understand patterns, trends, and distributions using Exploratory Data Analysis (EDA) techniques.

## Project Objective

The objective of this project is to examine the dataset, identify important characteristics, detect trends and outliers, and summarize key observations that can support data-driven decision-making.

## Key Requirements

- Calculate basic statistics (Mean, Median, Count)
- Identify trends in the dataset
- Detect outliers
- Summarize key observations
- Generate analytical reports

## Key Skills Demonstrated

- Data Analysis
- Descriptive Statistics
- Exploratory Data Analysis (EDA)
- Trend Identification
- Outlier Detection
- Analytical Thinking
- Report Generation

## Technologies Used

- Python
- Pandas
- NumPy
- OpenPyXL

## Features Implemented

### Data Loading
- Reads dataset from Excel files
- Automatically detects columns

### Statistical Analysis
Calculates:
- Count
- Mean
- Median
- Standard Deviation
- Minimum Value
- Maximum Value

### Missing Value Analysis
- Detects missing values
- Provides column-wise missing value summary

### Outlier Detection
Uses the Interquartile Range (IQR) method to:
- Detect unusual observations
- Calculate outlier percentages
- Generate outlier reports

### Trend Analysis
- Detects date columns automatically
- Analyzes monthly trends
- Identifies increasing, decreasing, or stable patterns

### Distribution Analysis
- Examines categorical variables
- Displays category frequencies
- Identifies dominant categories

## Outputs Generated

### Analysis Report
`project2_analysis_report.txt`

Contains:
- Dataset overview
- Missing value summary
- Trend analysis
- Key observations

### Numeric Statistics Report
`project2_numeric_statistics.csv`

Contains:
- Mean
- Median
- Count
- Standard deviation
- Minimum and maximum values

### Outlier Summary
`project2_outlier_summary.csv`

Contains:
- Outlier counts
- Outlier percentages

## Workflow

1. Load dataset
2. Check data quality
3. Detect date and numeric columns
4. Calculate descriptive statistics
5. Identify outliers
6. Analyze trends
7. Summarize observations
8. Generate reports

## Learning Outcomes

Through this project, the following concepts were applied:

- Exploratory Data Analysis (EDA)
- Descriptive Statistics
- Data Quality Assessment
- Trend Analysis
- Outlier Detection
- Business-Oriented Data Interpretation

## How to Run

Install required libraries:

```bash
pip install pandas numpy openpyxl
```

Run the program:

```bash
python project2.py
```

## Author

Ayesha Asna
DecodeLabs Internship
